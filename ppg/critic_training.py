from ppg.losses import value_loss_fun
from utils.logger import log_critic

from utils.network_utils import do_gradient_step, do_accumulated_gradient_step


def train_critic_batch(agent, states, expected_returns, old_state_values,
                       batch_idx, num_batches):
    config = agent.config
    state_values = agent.critic(states)
    critic_loss = value_loss_fun(state_values=state_values,
                                 old_state_values=old_state_values,
                                 expected_returns=expected_returns,
                                 is_aux_epoch=agent.trajectory.is_aux_epoch,
                                 value_clip=config['value_clip'])

    #do_gradient_step(agent.critic, agent.critic_opt, critic_loss, config[
    #    'grad_norm'])
    do_accumulated_gradient_step(agent.critic, agent.critic_opt, critic_loss,
                                 config, batch_idx, num_batches)

    if agent.use_wandb:
        log_critic(agent, critic_loss, state_values)
