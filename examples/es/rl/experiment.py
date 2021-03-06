from lagom.experiment import Configurator
from lagom.experiment import BaseExperimentWorker
from lagom.experiment import BaseExperimentMaster
from lagom.experiment import run_experiment

from algo import Algorithm


class ExperimentWorker(BaseExperimentWorker):
    def prepare(self):
        pass
        
    def make_algo(self):
        algo = Algorithm()
        
        return algo


class ExperimentMaster(BaseExperimentMaster):
    def make_configs(self):
        configurator = Configurator('grid')
        
        configurator.fixed('cuda', True)  # ES for small net, do not use GPU
        
        configurator.fixed('env.id', 'Pendulum-v0')
        configurator.fixed('env.standardize', False)  # whether to use VecStandardize
        
        configurator.fixed('network.recurrent', False)
        configurator.fixed('network.hidden_sizes', [32])
        
        configurator.fixed('es.algo', 'CMAES')
        configurator.fixed('es.popsize', 64)
        configurator.fixed('es.mu0', 0.0)
        configurator.fixed('es.std0', 0.5)
        
        """Hyperparameter search, later time
        configurator.grid('env.id', ['Pendulum-v0', 'Reacher-v2', 'InvertedPendulum-v2', 'HumanoidStandup-v2'])
        
        configurator.grid('network.hidden_size', [[32], [32, 32], [64, 64]])
        
        configurator.grid('es.popsize', [8, 16, 32, 64])
        configurator.grid('es.mu0', [0.0, 0.3, 0.5])
        configurator.grid('es.std0', [0.1, 0.5, 1.0])
        """
        configurator.fixed('train.num_iteration', 5000)
        configurator.fixed('train.N', 5)
        # we do not provide train.T because it internally uses env_spec.T
        
        configurator.fixed('log.interval', 10)
        configurator.fixed('log.dir', 'logs')

        list_config = configurator.make_configs()
        
        return list_config
    
    def make_seeds(self):
        list_seed = [1770966829, 1500925526, 2054191100]
        
        return list_seed
    
    def process_results(self, results):
        assert all([result is None for result in results])

        
if __name__ == '__main__':
    run_experiment(worker_class=ExperimentWorker, 
                   master_class=ExperimentMaster, 
                   num_worker=100)
