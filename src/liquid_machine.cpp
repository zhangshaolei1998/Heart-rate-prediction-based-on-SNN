#include <carlsim.h>
#include <spikegen_from_vector.h>
#include <poisson_rate.h>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <string.h>

#define neurNum 80
#define period 600
#define SI 100

using std::ifstream;
using std::ofstream;
using std::endl;
using std::vector;
using std::string;
using std::cout;

int spike_Monitor[neurNum][period]= {0};
vector<int> spikeTimes;

int main(int argc, const char* argv[]) {
	// ---------------- CONFIG STATE -------------------
	CARLsim sim("spnet", GPU_MODE, USER, 2, 42);

	int nNeur = 80;			// number of neurons
	int nInput = 0.8*nNeur;
	int nNeurExc = 0.8*nNeur;	// number of excitatory neurons
	int nNeurInh = 0.2*nNeur;	// number of inhibitory neurons
	//int nSynPerNeur = 100;  	// number of synpases per neuron
	int maxDelay = 2;      	// maximal conduction delay
	
	
	/*input*/
	char file[1][100];
	strcpy(file[0],"src/ECG_PRO/heartSimulation/ECG_72_10min_250HZ_op.txt");
	int startTime[] = {0};
	int stopTime[] = {60000};
	int fileNum = 1;
	int continueTime = 0;
	cout << endl<<endl<<endl;	
	for(int i = 0; i < fileNum; i++){
		cout << "reading " << file[i] <<endl;
		ifstream infile;
		infile.open(file[i]);
		int spikePosition;
		while(!infile.eof()){
			infile>>spikePosition;
			if(spikePosition <= startTime[i])
				continue;
			if(spikePosition > stopTime[i])
				break;
			spikeTimes.push_back(spikePosition - startTime[i] + continueTime);
		}
		continueTime += stopTime[i] - startTime[i];
		infile.close();
	}
	for(int i = 0; i < spikeTimes.size(); i++){
		cout << spikeTimes[i]<< " ";
	}	

	// create 80-20 network with 80% RS and 20% FS neurons
	int gInput = sim.createSpikeGeneratorGroup("input", nInput, EXCITATORY_POISSON);
	int gExc = sim.createGroup("exc", nNeurExc, EXCITATORY_NEURON);
	sim.setNeuronParameters(gExc, 0.02f, 0.2f, -65.0f, 8.0f); // RS
	int gInh = sim.createGroup("inh", nNeurInh, INHIBITORY_NEURON);
	sim.setNeuronParameters(gInh, 0.1f, 0.2f, -65.0f, 2.0f); // FS

	float W0 = 0.1f;
	//float wtExc = 6.0f;                   // synaptic weight magnitude if pre is exc
	//float wtInh = 5.0f;                   // synaptic weight magnitude if pre is inh (no negative sign)
	float wtMax = 10 * W0;                  // maximum synaptic weight magnitude
	//float pConn = nSynPerNeur*1.0f/nNeur; // connection probability

	//connect gInput and gExc by one-to-one
	sim.connect(gInput, gExc, "full", RangeWeight(1), 0.6, RangeDelay(1,2), RadiusRF(-1),SYN_FIXED);

	// gExc receives input from nSynPerNeur neurons from both gExc and gInh
	// every neuron in gExc should receive ~nSynPerNeur synapses

	//Synaptic connection delays are selected randomly between 1ms and 2ms.
	sim.connect(gExc, gExc, "full", RangeWeight(0.0f, W0, wtMax), 0.01f, RangeDelay(1,2), RadiusRF(-1), SYN_PLASTIC);
	sim.connect(gInh, gExc, "full", RangeWeight(0.0f, W0, wtMax), 0.1f, RangeDelay(1,2), RadiusRF(-1), SYN_PLASTIC);

	// gInh receives input from nSynPerNeur neurons from gExc, all delays are 1ms, no plasticity
	// every neuron in gInh should receive ~nSynPerNeur synapses
	sim.connect(gExc, gInh, "full", RangeWeight(0.0f, W0, wtMax), 0.1f, RangeDelay(1,2), RadiusRF(-1), SYN_PLASTIC);

	// enable STDP on all incoming synapses to gExc
	float alphaPlus = 0.1f, tauPlus = 20.0f, alphaMinus = 0.1f, tauMinus = 20.0f;
	sim.setESTDP(gExc, true, STANDARD, ExpCurve(alphaPlus, tauPlus, -alphaMinus, tauMinus));
	sim.setISTDP(gExc, true, STANDARD, ExpCurve(-alphaPlus, tauPlus, alphaMinus, tauMinus));
	sim.setESTDP(gInh, true, STANDARD, ExpCurve(alphaPlus, tauPlus, -alphaMinus, tauMinus));

	/*
		// set E-STDP parameters.
		float alpha_LTP=0.001f/5; float tau_LTP=20.0f;
		float alpha_LTD=0.00033f/5; float tau_LTD=60.0f;

		// set E-STDP to be STANDARD (without neuromodulatory influence) with an EXP_CURVE type.
		sim.setESTDP(gExc, true, STANDARD, ExpCurve(alpha_LTP, tau_LTP, -alpha_LTD, tau_LTD));

	*/

	// run CUBA mode
	sim.setConductances(true);

	// homeostasis constants for excitatory neurons
	float alpha = 0.1; // homeostatic scaling factor

	float T_exc = 10.0; // homeostatic time constant
	float R_target_exc = 35.0; // target firing rate neuron tries to achieve

	sim.setHomeostasis(gExc,true,alpha,T_exc);
	sim.setHomeoBaseFiringRate(gExc,R_target_exc);

	// homeostasis constants for inhibitory neurons
	float T_inh = 2.0; // homeostatic time constant
	float R_target_inh = 3.5; // target firing rate neuron tries to achieve

	sim.setHomeostasis(gInh,true,alpha,T_inh);
	sim.setHomeoBaseFiringRate(gInh,R_target_inh);

	// ---------------- SETUP STATE -------------------
	
	SpikeGeneratorFromVector SGV(spikeTimes);
	// associate group g0 with PSG
	sim.setSpikeGenerator(gInput, &SGV);

	sim.setupNetwork();
	//PoissonRate poissRate(nInput, true);
	//poissRate.setRates(13.0f);
	
	//sim.setSpikeGenerator(gInput, &SGV);
	//sim.setSpikeRate(gInput, &poissRate);

	SpikeMonitor* SMinput = sim.setSpikeMonitor(gInput, "NULL"); 
	SpikeMonitor* SMexc = sim.setSpikeMonitor(gExc, "NULL");
	SpikeMonitor* SMinh = sim.setSpikeMonitor(gInh, "NULL");
	ConnectionMonitor* CMine = sim.setConnectionMonitor(gInput,gExc,"DEFAULT");
	ConnectionMonitor* CMee = sim.setConnectionMonitor(gExc, gExc, "DEFAULT");
	ConnectionMonitor* CMei = sim.setConnectionMonitor(gInh, gExc, "DEFAULT");

	//CM->setUpdateTimeIntervalSec(-1);

	// ---------------- RUN STATE -------------------



	// take a snapshot of the weights before we run the simulation
	//CMei->takeSnapshot();
	//CMee->takeSnapshot();

	
	for(int i=0; i<period; i++) {
		SMexc->startRecording();
		SMinh->startRecording();
		sim.runNetwork(0, 100);
		SMexc->stopRecording();
		SMinh->stopRecording();
		for(int j=0; j<nNeurExc; j++) {
			spike_Monitor[j][i]=SMexc->getNeuronNumSpikes(j);
		}
		for(int j=0; j<nNeurInh; j++) {
			spike_Monitor[j + nNeurExc][i]=SMinh->getNeuronNumSpikes(j);
		}
	}

	/*readout unit*/
	ofstream ofs("src/ECG_PRO/spike.txt");
	for(int i=0; i<nNeur; i++) {
		for(int j=0; j<period; j++) {
			ofs<<spike_Monitor[i][j];
			if(j<period-1) ofs<<",";
		}
		ofs<<endl;
	}
	ofs.close();
	return 0;
}
