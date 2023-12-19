# CURSE YOU VALVE FOR NOT USING JSON!
# WHAT THE HELL IS THIS FORMAT, YOU JERKS
# THIS MADE THE SOLUTION MUCH MORE ANNOYING TO CODE
# AS I COULDN'T JUST PARSE THIS STUFF AS JSON
# LIFE IS PAIN

import os

# Root directory where user data is stored
root_directory = "C:\\Program Files (x86)\\Steam\\userdata"

# Function to change file permissions
def change_permissions(file_path, mode):
    os.chmod(file_path, mode)

# Function to modify the data
def setup_settings():
    settings = {
        # set up 1280x960 resolution
        "setting.defaultres":   "1280",
        "setting.defaultresheight": "960",

        # enable ambient occlusion
        "setting.r_aoproxy_enable": "1",
        "setting.r_aoproxy_min_dist":   "3",
        "setting.r_ssao":   "1",

        # set shader quality to lowest
        "settings.shaderquality":   "0",

        # allow player shadows, despite low quality shadows
        "setting.lb_enable_shadow_casting": "1",
        # make the player shadows sharper, 
        # (lowest value 0.1 - blurry, highest 0.4 - sharp, values above 0.4 disable casting shadows)
        # (might be resolution dependant tho, some people recommend value of 0.5, but for me it just disabled shadows)
        "setting.lb_barnlight_shadowmap_scale": "0.40000",

        # tweak player shadow resolution
        # NOTE: lower values prevent player shadows from being rendered! 
        # some tweakers recommend 2048x3072
        "setting.lb_shadow_texture_width_override":     "1280",
	    "setting.lb_shadow_texture_height_override":    "1280",

        # setup custom fsr resolution
        "setting.r_csgo_fsr_upsample":  "2",
        # this is for tweaking the custom scaling. 
        # can be set to 0.1 (10% resolution) if you're crazy, 
        # didn't test lower values for my sanity
        # fsr performance is 0.5
        "setting.mat_viewportscale":    "0.400000",

        # enable nvidia reflex. (non boost)
        "setting.r_low_latency": "1",

        # disable view model shadows
        "setting.csm_viewmodel_shadows": "0",

        # if lowend objects available, use them
        # I'm not sure if this does anything but why not. 
        "setting.r_csgo_lowend_objects": "1",

        # particle shadows? lol nah.
        "setting.r_particle_shadows": "0",

        # set textures to lowest
        "setting.r_texturefilteringquality": "0",

        # these values are clamped, but I'm not sure to what values, 
        # so just setting them to 64 and letting the game figure it out
        # https://www.reddit.com/r/GlobalOffensive/comments/16uwozc/release_notes_for_9282023/
        "setting.r_character_decal_resolution": "64",
	    "setting.r_texture_stream_max_resolution": "64",

        # disable CMAA and MSAA
        "setting.r_csgo_cmaa_enable": "0",
        "setting.msaa_samples": "0",
    }
    return settings

def modify_config_values(file_path, new_values):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            for key, new_value in new_values.items():
                if line.strip().startswith(f'"{key}"'):
                    updated_line = f'\t"{key}"\t\t"{new_value}"\n'
                    file.write(updated_line)
                    break
            else:
                file.write(line)




# Recursive function to find and modify the video.cfg file
def find_and_modify_video_cfg(directory):
    for user_folder in os.listdir(directory):
        user_folder_path = os.path.join(directory, user_folder)
        if os.path.isdir(user_folder_path):
            cfg_path = os.path.join(user_folder_path, "730\\local\\cfg\\cs2_video.txt")
            if os.path.exists(cfg_path):
                print(f"Modified {cfg_path}")

                # Change file permissions to make it writable
                change_permissions(cfg_path, 0o777) 

                # Parse the lines to get key-value pairs
                settings = setup_settings()

                # Read file, parse it, write new values
                modify_config_values(cfg_path, settings)

                # Change file permissions back to read-only
                change_permissions(cfg_path, 0o444)  # Change file permissions to read-only

# Start searching for video.cfg files
find_and_modify_video_cfg(root_directory)
