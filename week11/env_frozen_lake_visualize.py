import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import patheffects as pe
from IPython.display import clear_output


TILE_STYLES = {
    "S": {"label": "S", "color": "#ffffff", "text_color": "#023047"},
    "F": {"label": "F", "color": "#caf0f8", "text_color": "#03045e"},
    "H": {"label": "H", "color": "#6c757d", "text_color": "white"},
    "G": {"label": "G", "color": "#90be6d", "text_color": "#1b4332"},
}

ACTION_LAYOUT = {
    "left": {"arrow": (-0.15, 0.0), "edge_center": (0.18, 0.5)},
    "down": {"arrow": (0.0, 0.15), "edge_center": (0.5, 0.82)},
    "right": {"arrow": (0.15, 0.0), "edge_center": (0.82, 0.5)},
    "up": {"arrow": (0.0, -0.15), "edge_center": (0.5, 0.18)},
}

OUTCOME_LAYOUT = {
    "left": {"delta": (-0.15, 0.0), "label_shift": (-0.12, 0.06)},
    "down": {"delta": (0.0, 0.15), "label_shift": (0.07, 0.12)},
    "right": {"delta": (0.15, 0.0), "label_shift": (0.12, -0.06)},
    "up": {"delta": (0.0, -0.15), "label_shift": (-0.07, -0.12)},
}

MOVE_TO_ACTION = {
    (-1, 0): "up",
    (1, 0): "down",
    (0, -1): "left",
    (0, 1): "right",
    (0, 0): "stay",
}

Q_VALUE_LAYOUT = {
    "left": (0.18, 0.5),
    "down": (0.5, 0.82),
    "right": (0.82, 0.5),
    "up": (0.5, 0.18),
}


def is_grid_state(state):
    return isinstance(state, tuple) and len(state) == 2


def _draw_grid(ax, env):
    desc = np.asarray(env.desc)
    nrow, ncol = desc.shape
    ax.set_xlim(0, ncol)
    ax.set_ylim(nrow, 0)
    ax.set_aspect("equal")

    for row in range(nrow):
        for col in range(ncol):
            tile = desc[row, col]
            style = TILE_STYLES[tile]
            ax.add_patch(
                Rectangle((col, row), 1, 1, facecolor=style["color"], edgecolor="white", linewidth=2)
            )
            ax.text(
                col + 0.1,
                row + 0.14,
                style["label"],
                ha="left",
                va="center",
                fontsize=14,
                fontweight="bold",
                color=style["text_color"],
            )

    ax.set_xticks(np.arange(ncol + 1))
    ax.set_yticks(np.arange(nrow + 1))
    ax.grid(color="white", linewidth=2)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(length=0)
    return desc


def _circle_label(ax, x, y, text, facecolor="white", edgecolor="#1d3557", text_color="#1d3557", fontsize=8.5, zorder=7):
    circle_text = ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight="bold",
        color=text_color,
        bbox=dict(boxstyle="circle,pad=0.18", facecolor=facecolor, edgecolor=edgecolor, linewidth=1.0),
        zorder=zorder,
    )
    circle_text.set_path_effects([pe.withStroke(linewidth=2.0, foreground="white")])
    return circle_text


def _get_q_value_map(q_values, state, actions):
    state_values = q_values[state]
    if isinstance(state_values, dict):
        return {action: float(state_values[action]) for action in actions}
    return {action: float(state_values[idx]) for idx, action in enumerate(actions)}


def _get_state_value(q_values, state):
    state_values = q_values[state]
    if isinstance(state_values, dict):
        return max(state_values.values())
    return float(np.max(state_values))


def _draw_agent_marker(ax, state, zorder=9):
    if not is_grid_state(state):
        return
    agent_row, agent_col = state
    ax.scatter(agent_col + 0.5, agent_row + 0.5, s=340, c="#d62828", edgecolors="white", linewidths=1.3, zorder=zorder)
    ax.text(agent_col + 0.5, agent_row + 0.5, "A", ha="center", va="center", fontsize=9, fontweight="bold", color="white", zorder=zorder + 1)


def _draw_trajectory(ax, trajectory):
    if not trajectory:
        return

    current_segment = []
    for state in trajectory:
        if is_grid_state(state):
            current_segment.append((state[1] + 0.5, state[0] + 0.5))
        else:
            if len(current_segment) >= 2:
                xs, ys = zip(*current_segment)
                ax.plot(xs, ys, color="#d62828", linewidth=2.2, alpha=0.6, zorder=10)
            current_segment = []

    if len(current_segment) >= 2:
        xs, ys = zip(*current_segment)
        ax.plot(xs, ys, color="#d62828", linewidth=2.2, alpha=0.6, zorder=10)


def moving_average(values, window=100):
    if len(values) == 0:
        return np.array([])
    values = np.asarray(values, dtype=float)
    averages = np.empty(len(values))
    for i in range(len(values)):
        start = max(0, i - window + 1)
        averages[i] = values[start:i + 1].mean()
    return averages


def env_frozen_lake_training_visualize(
    env,
    q_values,
    rewards_history,
    episode_n,
    title,
    trajectory=None,
    agent_state=None,
    active_state=None,
    selected_action=None,
    updated_state=None,
    updated_action=None,
    clear=True,
):
    if clear:
        clear_output(wait=True)

    grid_states = [(row, col) for row in range(env.desc.shape[0]) for col in range(env.desc.shape[1])]
    value_function = {state: _get_state_value(q_values, state) for state in grid_states}

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(11.5, 5.6),
        gridspec_kw={"width_ratios": [1.2, 1.0]},
    )
    env_frozen_lake_q_values_visualize(
        env,
        q_values,
        state_values=value_function,
        ax=axes[0],
        title=title,
        agent_state=agent_state,
        active_state=active_state,
        selected_action=selected_action,
        updated_state=updated_state,
        updated_action=updated_action,
        trajectory=trajectory,
    )

    reward_axis = axes[1]
    reward_axis.set_title("Total reward per episode", fontsize=12)
    reward_axis.set_xlabel("Episode")
    reward_axis.set_ylabel("Reward")
    reward_axis.set_xlim(1, episode_n)
    reward_axis.set_ylim(-0.05, 1.05)

    if len(rewards_history) > 0:
        x = np.arange(1, len(rewards_history) + 1)
        reward_axis.plot(x, rewards_history, color="#8d99ae", linewidth=1.6, label="reward")
        reward_axis.plot(x, moving_average(rewards_history, window=100), color="#d62828", linewidth=2.2, label="mean(100)")
        reward_axis.legend(loc="upper left")

    reward_axis.grid(alpha=0.25)
    plt.tight_layout()
    plt.show()


def env_frozen_lake_visualize(
    env,
    state=None,
    ax=None,
    active_state=None,
    selected_action=None,
    realized_move=None,
    transition_probability=True,
):
    desc = np.asarray(env.desc)
    nrow, ncol = desc.shape
    created_figure = ax is None
    state = env._current_state if state is None else state

    if created_figure:
        _, ax = plt.subplots(figsize=(2.7 * ncol, 2.7 * nrow))

    _draw_grid(ax, env)

    for row in range(nrow):
        for col in range(ncol):
            cell_state = (row, col)

            if env.is_terminal(cell_state) or not transition_probability:
                continue

            center_x = col + 0.5
            center_y = row + 0.5

            for action in env.get_possible_actions(cell_state):
                action_layout = ACTION_LAYOUT[action]
                dx, dy = action_layout["arrow"]
                is_selected_action = cell_state == active_state and action == selected_action
                action_color = "#d62828" if is_selected_action else "#1d3557"
                ax.annotate(
                    "",
                    xy=(center_x + dx, center_y + dy),
                    xytext=(center_x, center_y),
                    arrowprops=dict(arrowstyle="->", lw=2.1, color=action_color),
                    zorder=4,
                )

                edge_x = col + action_layout["edge_center"][0]
                edge_y = row + action_layout["edge_center"][1]
                transition_probs = {key: 0.0 for key in OUTCOME_LAYOUT}
                stay_prob = 0.0
                terminal_prob = 0.0
                for next_state, prob in sorted(env.get_next_states(cell_state, action).items()):
                    if not is_grid_state(next_state):
                        terminal_prob += prob
                        continue
                    next_row, next_col = next_state
                    move_key = MOVE_TO_ACTION[(next_row - row, next_col - col)]
                    if move_key == "stay":
                        stay_prob = prob
                        continue
                    transition_probs[move_key] = prob

                for move_key, outcome_layout in OUTCOME_LAYOUT.items():
                    is_realized_move = (
                        cell_state == active_state and action == selected_action and move_key == realized_move
                    )
                    alpha = 0.18 + 0.82 * transition_probs[move_key]
                    odx, ody = outcome_layout["delta"]
                    ax.annotate(
                        "",
                        xy=(edge_x + odx, edge_y + ody),
                        xytext=(edge_x, edge_y),
                        arrowprops=dict(
                            arrowstyle="->",
                            lw=2.1,
                            color="#d62828" if is_realized_move else "#1d3557",
                            alpha=1.0 if is_realized_move else alpha,
                        ),
                        zorder=4,
                    )
                    label_x = edge_x + outcome_layout["label_shift"][0]
                    label_y = edge_y + outcome_layout["label_shift"][1]
                    prob_text = ax.text(
                        label_x,
                        label_y,
                        f"{transition_probs[move_key]:.1f}",
                        ha="center",
                        va="center",
                        fontsize=8.5,
                        color="#d62828" if is_realized_move else "#1d3557",
                        alpha=1.0 if is_realized_move else alpha,
                        zorder=5,
                    )
                    prob_text.set_path_effects([pe.withStroke(linewidth=2.3, foreground="white")])

                stay_display_prob = terminal_prob if terminal_prob > 0 else stay_prob
                stay_alpha = 0.18 + 0.82 * stay_display_prob
                is_realized_stay = cell_state == active_state and action == selected_action and realized_move == "stay"
                stay_text = ax.text(
                    edge_x,
                    edge_y,
                    f"{stay_display_prob:.1f}",
                    ha="center",
                    va="center",
                    fontsize=8.5,
                    fontweight="bold",
                    color="#d62828" if is_realized_stay else "#1d3557",
                    alpha=1.0 if is_realized_stay else stay_alpha,
                    bbox=dict(
                        boxstyle="circle,pad=0.16",
                        facecolor="white",
                        edgecolor="#d62828" if is_realized_stay else "#1d3557",
                        linewidth=1.0,
                        alpha=1.0,
                    ),
                    zorder=7,
                )
                stay_text.set_path_effects([pe.withStroke(linewidth=2.3, foreground="white")])

    if is_grid_state(state):
        agent_row, agent_col = state
        ax.scatter(agent_col + 0.5, agent_row + 0.5, s=340, c="#d62828", edgecolors="white", linewidths=1.3, zorder=6)
        ax.text(agent_col + 0.5, agent_row + 0.5, "A", ha="center", va="center", fontsize=9, fontweight="bold", color="white", zorder=7)

    title = "Frozen Lake: Transition Probabilities" if transition_probability else "Frozen Lake"
    ax.set_title(title, fontsize=15, pad=12)

    if created_figure:
        plt.show()


def env_frozen_lake_random_policy_demo(env, delay=0.5, seed=0):
    from IPython.display import clear_output, display

    rng = np.random.default_rng(seed)
    state = env.reset()
    try:
        while True:
            fig, ax = plt.subplots(figsize=(2.7 * env.desc.shape[1], 2.7 * env.desc.shape[0]))
            env_frozen_lake_visualize(env, state=state, ax=ax)
            display(fig)
            plt.close(fig)
            time.sleep(delay)

            actions = env.get_possible_actions(state)
            if len(actions) == 0:
                state = env.reset()
                clear_output(wait=True)
                continue

            current_state = state
            action = actions[rng.integers(len(actions))]
            clear_output(wait=True)

            fig, ax = plt.subplots(figsize=(2.7 * env.desc.shape[1], 2.7 * env.desc.shape[0]))
            env_frozen_lake_visualize(
                env,
                state=current_state,
                ax=ax,
                active_state=current_state,
                selected_action=action,
            )
            display(fig)
            plt.close(fig)
            time.sleep(delay)

            state, reward, done, _ = env.step(action)
            if is_grid_state(state) and is_grid_state(current_state):
                realized_move = MOVE_TO_ACTION[(state[0] - current_state[0], state[1] - current_state[1])]
            else:
                realized_move = None
            clear_output(wait=True)

            fig, ax = plt.subplots(figsize=(2.7 * env.desc.shape[1], 2.7 * env.desc.shape[0]))
            env_frozen_lake_visualize(
                env,
                state=current_state,
                ax=ax,
                active_state=current_state,
                selected_action=action,
                realized_move=realized_move,
            )
            display(fig)
            plt.close(fig)
            time.sleep(delay)

            if done:
                clear_output(wait=True)
                fig, ax = plt.subplots(figsize=(2.7 * env.desc.shape[1], 2.7 * env.desc.shape[0]))
                env_frozen_lake_visualize(env, state=current_state, ax=ax)
                display(fig)
                plt.close(fig)
                time.sleep(delay)

                state = env.reset()
                clear_output(wait=True)
                continue

            clear_output(wait=True)

            fig, ax = plt.subplots(figsize=(2.7 * env.desc.shape[1], 2.7 * env.desc.shape[0]))
            env_frozen_lake_visualize(env, state=state, ax=ax)
            display(fig)
            plt.close(fig)

            time.sleep(delay)
            clear_output(wait=True)
    except KeyboardInterrupt:
        clear_output(wait=True)
        return


def env_frozen_lake_policy_visualize(env, values, policy, ax=None, iteration=None):
    desc = np.asarray(env.desc)
    nrow, ncol = desc.shape
    created_figure = ax is None

    if created_figure:
        _, ax = plt.subplots(figsize=(2.7 * ncol, 2.7 * nrow))

    _draw_grid(ax, env)

    for row in range(nrow):
        for col in range(ncol):
            cell_state = (row, col)

            value_text = _circle_label(
                ax,
                col + 0.5,
                row + 0.5,
                f"{values[cell_state]:.2f}",
            )

            if env.is_terminal(cell_state):
                continue

            center_x = col + 0.5
            center_y = row + 0.5

            for action in env.get_possible_actions(cell_state):
                action_layout = ACTION_LAYOUT[action]
                dx, dy = action_layout["arrow"]
                prob = policy[cell_state][action]
                alpha = 0.2 + 0.8 * prob
                ax.annotate(
                    "",
                    xy=(center_x + dx, center_y + dy),
                    xytext=(center_x, center_y),
                    arrowprops=dict(arrowstyle="->", lw=2.1, color="#1d3557", alpha=alpha),
                    zorder=4,
                )
                prob_text = ax.text(
                    center_x + dx * 1.18,
                    center_y + dy * 1.18,
                    f"{prob:.2f}",
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="#1d3557",
                    alpha=alpha,
                    zorder=5,
                )
                prob_text.set_path_effects([pe.withStroke(linewidth=2.0, foreground="white")])

    title = "Frozen Lake: Policy Iteration"
    if iteration is not None:
        title += f", iteration {iteration}"
    ax.set_title(title, fontsize=15, pad=12)

    if created_figure:
        plt.show()


def env_frozen_lake_q_values_visualize(
    env,
    q_values,
    state_values=None,
    ax=None,
    title="Frozen Lake: V(s) and Q(s, a)",
    agent_state=None,
    active_state=None,
    selected_action=None,
    updated_state=None,
    updated_action=None,
    trajectory=None,
):
    desc = np.asarray(env.desc)
    nrow, ncol = desc.shape
    created_figure = ax is None

    if created_figure:
        _, ax = plt.subplots(figsize=(3.1 * ncol, 3.1 * nrow))

    _draw_grid(ax, env)
    _draw_trajectory(ax, trajectory)

    for row in range(nrow):
        for col in range(ncol):
            cell_state = (row, col)
            actions = list(env.get_possible_actions(cell_state))
            center_x = col + 0.5
            center_y = row + 0.5
            tile = desc[row, col]

            if len(actions) == 0:
                continue

            q_value_map = _get_q_value_map(q_values, cell_state, actions)
            value = state_values[cell_state] if state_values is not None else max(q_value_map.values())
            show_center_value = tile not in {"H", "G"}
            show_side_values = tile not in {"H", "G"}

            if show_side_values:
                for action in actions:
                    action_layout = ACTION_LAYOUT[action]
                    dx, dy = action_layout["arrow"]
                    is_selected_action = cell_state == active_state and action == selected_action
                    ax.annotate(
                        "",
                        xy=(center_x + dx, center_y + dy),
                        xytext=(center_x, center_y),
                        arrowprops=dict(
                            arrowstyle="->",
                            lw=2.3,
                            color="#d62828" if is_selected_action else "#1d3557",
                        ),
                        zorder=4,
                    )

                    qx = col + Q_VALUE_LAYOUT[action][0]
                    qy = row + Q_VALUE_LAYOUT[action][1]
                    is_updated_q = cell_state == updated_state and action == updated_action
                    _circle_label(
                        ax,
                        qx,
                        qy,
                        f"{q_value_map[action]:.2f}",
                        facecolor="#ffe5e5" if is_updated_q else "#f8fbff",
                        edgecolor="#d62828" if is_updated_q else "#457b9d",
                        text_color="#d62828" if is_updated_q else "#1d3557",
                        fontsize=7.8,
                        zorder=8 if is_updated_q else 7,
                    )

            if show_center_value:
                _circle_label(
                    ax,
                    center_x,
                    center_y,
                    f"{value:.2f}",
                    facecolor="white",
                    edgecolor="#1d3557",
                    text_color="#1d3557",
                    fontsize=8.5,
                    zorder=8,
                )

    _draw_agent_marker(ax, agent_state if agent_state is not None else active_state)
    ax.set_title(title, fontsize=15, pad=12)

    if created_figure:
        plt.show()
