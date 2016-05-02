from heppy.framework.analyzer import Analyzer
from heppy.papas.pfalgo.alicepfreconstructor import AlicePFReconstructor as PFReconstructor
from heppy.papas.data.pfevent import PFEvent
from heppy.papas.pfalgo.distance  import Distance
from heppy.papas.data.history import History

class PapasPFReconstructor(Analyzer):

    def __init__(self, *args, **kwargs):
        super(PapasPFReconstructor, self).__init__(*args, **kwargs)
        #self.instance_label =  
        self.detector = self.cfg_ana.detector
        self.reconstructed = PFReconstructor(self.detector, self.mainLogger)
        self.blocksname =  self.cfg_ana.input_blocks
        self.input_historyname = self.cfg_ana.input_history
        self.output_historyname = self.cfg_ana.output_history   
        self.output_particlesdictname = '_'.join([self.instance_label, self.cfg_ana.output_particles_dict])
        self.output_particleslistname = '_'.join([self.instance_label, self.cfg_ana.output_particles_list])
                
    def process(self, event):
        ''' Calls the particle reconstruction algorithm and returns the 
           reconstructed paricles and updated history_nodes to the event object
           arguments:
                    event must contain blocks made using BlockBuilder'''
        
        self.reconstructed.reconstruct(event,  self.blocksname, self.input_historyname)
        
        setattr(event, self.output_historyname, self.reconstructed.history_nodes )
        setattr(event, self.output_particlesdictname, self.reconstructed.particles )
        
        #hist = History(event.history_nodes,PFEvent(event))
        #for block in event.blocks:
        #    hist.summary_of_links(block)
        
        #for particle comparison we want a list of particles (instead of a dict) so that we can sort and compare
        reconstructed_particle_list = sorted( self.reconstructed.particles.values(),
                                                   key = lambda ptc: ptc.e(), reverse=True)
        
        setattr(event, self.output_particleslistname, reconstructed_particle_list)
        pass         