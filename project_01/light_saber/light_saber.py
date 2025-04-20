from sLED_DotStar import DotStar
from sLED_Animations import Animations
import time

num_leds = 121  # SHOULD ALWAYS BE ODD

def base_color():
    return (255, 255, 255)  # Blue

# Create DotStar instance
dotstare = DotStar(num_leds=num_leds, brightness=1.0)

# Pass DotStar instance to Animations
sLED = Animations(dotstare)

# Test light_up function
print("Testing light_up animation...")
sLED.light_up(base_color=base_color, speed=0.05)
time.sleep(2)

# Test light_down function
print("Testing light_down animation...")
sLED.light_down(base_color=base_color, speed=0.05)
time.sleep(2)

# Clean up
dotstare.close()
