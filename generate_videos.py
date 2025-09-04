#!/usr/bin/env python3
import os
import sys
import gymnasium as gym
import time
import importlib.util
import traceback
import numpy as np

os.environ["MUJOCO_GL"] = "glfw"
os.environ["DISPLAY"] = ":99"


def load_policy(policy_path):
    """
    Dynamically load a policy module from a file and return its get_action function.
    """
    spec = importlib.util.spec_from_file_location("policy_module", policy_path)
    policy_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(policy_module)
    if hasattr(policy_module, "get_action"):
        return policy_module.get_action
    else:
        raise AttributeError(f"Module {policy_path} does not define get_action(observation)")

def list_video_files(directory):
    """Recursively list all .mp4 files in the given directory."""
    video_files = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp4'):
                video_files.add(os.path.join(root, file))
    return video_files

def record_video_for_policy(get_action, video_path, gym_env_name='InvertedPendulum-v4',num_episodes=1):
    """
    Run multiple episodes in the given gym environment controlled by the get_action function,
    record videos saved to video_path, and rename each video file to include the total reward.
    
    Parameters:
      - get_action: function taking observation and returning an action.
      - video_path: The target video file path (its directory will be used to store the videos).
      - gym_env_name: Name of the Gym environment.
      - num_episodes: Number of episodes to record.
      - timeout: Maximum time (in seconds) to wait for the video file to appear.
    """
    # Ensure the video directory exists.
    video_dir = os.path.dirname(video_path)
    if not os.path.exists(video_dir):
        os.makedirs(video_dir)
    
    # Use the base name (without extension) as the video name prefix.
    video_name_prefix = os.path.splitext(os.path.basename(video_path))[0]
    
    # Create the gym environment with a      mode that produces frames.
    env = gym.make(gym_env_name, render_mode="rgb_array")
    
    # Wrap the environment with RecordVideo.
    env = gym.wrappers.RecordVideo(
        env,
        video_dir,
        episode_trigger=lambda episode_id: True,
        name_prefix=video_name_prefix
    )
    
    for episode in range(num_episodes):
        print(f"Starting episode {episode+1}...")
        total_reward = 0.0
        
        # Get snapshot of existing video files (recursively).
        files_before = list_video_files(video_dir)
        
        observation, info = env.reset()
        done = False
        steps = 0
        
        while not done:
            # Handle different function signatures - some expect individual parameters, others expect the full observation
            try:
                # Try calling with unpacked observation (for functions expecting individual parameters)
                action = get_action(*observation)
            except TypeError:
                # Fall back to passing the full observation array
                action = get_action(observation)
            
            # Ensure action is properly formatted
            if isinstance(action, (list, np.ndarray)):
                action = action[0] if len(action) > 0 else 0.0
            
            # Handle discrete vs continuous action spaces
            if hasattr(env.action_space, 'low'):  # Continuous action space
                action = np.array([action], dtype=np.float32)
                action = np.clip(action, env.action_space.low, env.action_space.high)
            else:  # Discrete action space
                action = int(action)
                action = np.clip(action, 0, env.action_space.n - 1)
            
            result = env.step(action)
            # Handle both new (5-tuple) and old (4-tuple) return types.
            if len(result) == 5:
                observation, reward, done, truncated, info = result
                done = done or truncated
            else:
                observation, reward, done, info = result
            total_reward += reward
            steps += 1
        
        print(f"Episode {episode+1} complete. Total reward: {total_reward}")
        
        # Wait (polling) for a new video file to appear, with a timeout.
        start_time = time.time()
        new_file = None
        timeout = 10
        while time.time() - start_time < timeout:
            files_after = list_video_files(video_dir)
            new_files = files_after - files_before
            if new_files:
                # Choose the most recently modified file among the new ones.
                new_file = min(new_files, key=lambda f: os.path.getmtime(f))
                break
            time.sleep(0.2)
        
        if new_file:
            old_path = new_file
            # Create a new name that includes episode number and total reward.
            new_name = f"{video_name_prefix}-episode{episode+1}-reward{int(total_reward)}.mp4"
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            os.rename(old_path, new_path)
            print(f"Renamed video file to: {new_path}")
        else:
            print("No new video file found for this episode within the timeout period.")
    
    env.close()
    print("Recording complete.")
    print("Check the video directory:", video_dir)

def process_policies(root_path, gym_env_name):
    """
    Process each Python policy file found in the policies folder at the root directory.
    """
    policies_dir = os.path.join(root_path, "policies")
    videos_dir = os.path.join(root_path, "videos")
    
    if not os.path.isdir(policies_dir):
        print(f"No policies directory found in {root_path}.")
        return
    else:
        print(f"Processing policies in: {policies_dir}")
    
    if not os.path.exists(videos_dir):
        os.makedirs(videos_dir)
        print(f"Created videos directory: {videos_dir}")
    
    for filename in os.listdir(policies_dir):
        if filename.endswith(".py"):
            policy_path = os.path.join(policies_dir, filename)
            print(f"Found policy: {policy_path}")
            try:
                get_action = load_policy(policy_path)
            except Exception as e:
                print(f"Error loading {policy_path}: {e}")
                traceback.print_exc()
                continue

            # Save the video with the same base name as the policy file.
            video_filename = os.path.splitext(filename)[0] + ".mp4"
            video_path = os.path.join(videos_dir, video_filename)
            
            print(f"Recording video for policy: {policy_path}")
            try:
                record_video_for_policy(get_action, video_path, gym_env_name,5)
                print(f"Saved video to: {video_path}")
            except Exception as e:
                print(f"Error recording video for {policy_path}: {e}")
                traceback.print_exc()

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_videos.py <root_path> [gym_env_name]")
        sys.exit(1)
    
    root_path = sys.argv[1]
    gym_env_name = sys.argv[2] if len(sys.argv) > 2 else "CartPole-v1"
    process_policies(root_path, gym_env_name)

if __name__ == "__main__":
    main()