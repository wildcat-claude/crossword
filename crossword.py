"""
Crossword Puzzle App — single-file tkinter implementation
"""

# ─────────────────────────────────────────────────────────────
# 1. IMPORTS & CONSTANTS
# ─────────────────────────────────────────────────────────────
import tkinter as tk
from tkinter import font as tkfont
import random
import time
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Dict

DIFFICULTY_SETTINGS = {
    "Easy":   {"size": 9,  "word_count": 12, "min_len": 3, "max_len": 5},
    "Medium": {"size": 13, "word_count": 20, "min_len": 4, "max_len": 7},
    "Hard":   {"size": 15, "word_count": 28, "min_len": 5, "max_len": 12},
}

COLORS = {
    "black_cell":     "#1a1a1a",
    "white_cell":     "#ffffff",
    "selected_cell":  "#f5c518",
    "word_highlight": "#b8d4f0",
    "correct_cell":   "#a8e6a3",
    "revealed_cell":  "#d4b8f0",
    "error_text":     "#cc0000",
    "normal_text":    "#000000",
    "number_text":    "#333333",
    "toolbar_bg":     "#2d2d2d",
    "toolbar_fg":     "#ffffff",
    "clue_active":    "#4a90d9",
    "clue_bg":        "#f5f5f5",
}

MARGIN = 2
CELL_MIN = 28


# ─────────────────────────────────────────────────────────────
# 2. WORD BANKS
# ─────────────────────────────────────────────────────────────
WORD_BANKS: Dict[str, List[Tuple[str, str]]] = {

"Easy": [
    ("CAT",  "Common household pet"),
    ("DOG",  "Man's best friend"),
    ("SUN",  "Star at center of our solar system"),
    ("MAP",  "Navigation aid"),
    ("CUP",  "Drinking vessel"),
    ("HAT",  "Head covering"),
    ("BAG",  "Carrying container"),
    ("BUS",  "Public transport vehicle"),
    ("FAN",  "Cooling device or enthusiast"),
    ("JAM",  "Fruit preserve"),
    ("LOG",  "Piece of cut wood"),
    ("MOP",  "Floor cleaning tool"),
    ("NET",  "Mesh used in sports"),
    ("PAN",  "Flat cooking vessel"),
    ("RUG",  "Floor covering"),
    ("SAP",  "Tree fluid"),
    ("TAB",  "Small flap or label"),
    ("VAT",  "Large container"),
    ("WAX",  "Candle material"),
    ("ZAP",  "To strike with electricity"),
    ("ACE",  "Top playing card"),
    ("BED",  "Sleeping furniture"),
    ("COT",  "Small portable bed"),
    ("DEN",  "Small cozy room"),
    ("EGG",  "Oval breakfast food"),
    ("FIG",  "Sweet Mediterranean fruit"),
    ("GEM",  "Precious stone"),
    ("HEN",  "Female chicken"),
    ("INK",  "Writing fluid"),
    ("JET",  "Fast aircraft"),
    ("KEG",  "Small barrel"),
    ("LAP",  "Top of seated person's legs"),
    ("MUD",  "Wet earth"),
    ("NUT",  "Hard-shelled seed"),
    ("OAK",  "Common hardwood tree"),
    ("PEA",  "Small round green vegetable"),
    ("QUE",  "Line of people waiting"), # note: typically QUEUE but keeping 3 letter
    ("ROW",  "Line of seats"),
    ("SOB",  "Cry loudly"),
    ("TAP",  "Faucet or light knock"),
    ("URN",  "Decorative vase"),
    ("VAN",  "Cargo vehicle"),
    ("WIG",  "Artificial hair piece"),
    ("YAK",  "Himalayan bovine"),
    ("ZEN",  "Buddhist meditation tradition"),
    ("ARM",  "Limb attached to shoulder"),
    ("BOX",  "Rectangular container"),
    ("CAP",  "Brimless hat"),
    ("DIP",  "Brief immersion or sauce"),
    ("ELM",  "Common shade tree"),
    ("FLY",  "Winged insect"),
    ("GUN",  "Weapon that fires projectiles"),
    ("HOP",  "Small jump"),
    ("IVY",  "Climbing plant"),
    ("JAB",  "Quick punch"),
    ("KIT",  "Set of tools"),
    ("LIP",  "Edge of mouth"),
    ("MAT",  "Small floor covering"),
    ("NOD",  "Head movement of agreement"),
    ("OWL",  "Nocturnal bird"),
    ("PIT",  "Deep hole"),
    ("RAT",  "Rodent"),
    ("SAW",  "Cutting tool"),
    ("TIP",  "End point or gratuity"),
    ("VET",  "Animal doctor"),
    ("WEB",  "Spider's creation"),
    ("YEW",  "Evergreen tree"),
    ("APE",  "Large primate"),
    ("BEE",  "Honey-making insect"),
    ("COW",  "Dairy farm animal"),
    ("DIM",  "Not very bright"),
    ("EEL",  "Snake-like fish"),
    ("FOX",  "Clever canine"),
    ("GAP",  "Opening or space"),
    ("HUB",  "Center of a wheel"),
    ("ICE",  "Frozen water"),
    ("JOG",  "Slow run"),
    ("KEY",  "Opens a lock"),
    ("LEG",  "Limb for walking"),
    ("MOB",  "Unruly crowd"),
    ("NAP",  "Short sleep"),
    ("ODD",  "Strange or not even"),
    ("POD",  "Seed container"),
    ("RIB",  "Chest bone"),
    ("SUB",  "Submarine or substitute"),
    ("TON",  "Unit of heavy weight"),
    ("USE",  "Put to work"),
    ("VIA",  "By way of"),
    ("WOE",  "Great sorrow"),
    ("YAM",  "Sweet orange root vegetable"),
    ("ZAG",  "Turn in opposite direction"),
    ("CAKE", "Baked sweet dessert"),
    ("BOAT", "Small watercraft"),
    ("CAVE", "Underground hollow"),
    ("DOVE", "Peaceful bird"),
    ("EDGE", "Outer boundary"),
    ("FACE", "Front of the head"),
    ("GAME", "Activity with rules"),
    ("HIVE", "Bee colony home"),
    ("IRON", "Metal used for pressing clothes"),
    ("JOKE", "Something said for laughs"),
    # ── Extra Easy words ──
    ("ACT",  "Perform on stage"),
    ("AID",  "Help or assistance"),
    ("AIM",  "Point toward a goal"),
    ("AIR",  "What we breathe"),
    ("AXE",  "Wood-chopping tool"),
    ("BAR",  "Place to get drinks"),
    ("BAT",  "Flying mammal or sports stick"),
    ("BOW",  "Archer's weapon"),
    ("BUN",  "Round bread roll"),
    ("CRY",  "Shed tears"),
    ("CUT",  "Slice with a blade"),
    ("DAD",  "Father informally"),
    ("DAY",  "24-hour period"),
    ("DRY",  "Not wet"),
    ("EAR",  "Organ for hearing"),
    ("EWE",  "Female sheep"),
    ("EYE",  "Organ for seeing"),
    ("FAR",  "Not nearby"),
    ("FAT",  "Plump or cooking grease"),
    ("FLU",  "Winter illness"),
    ("FUN",  "Enjoyment"),
    ("GAS",  "Fuel for cars"),
    ("HAM",  "Cured pork"),
    ("HIT",  "Strike hard"),
    ("HUG",  "Warm embrace"),
    ("JAR",  "Glass storage container"),
    ("JOY",  "Feeling of happiness"),
    ("LAD",  "Young boy"),
    ("LAW",  "Rule enforced by courts"),
    ("MAN",  "Adult male"),
    ("MAY",  "Fifth month"),
    ("MIX",  "Combine together"),
    ("OAR",  "Paddle for a boat"),
    ("OAT",  "Grain for porridge"),
    ("OWE",  "Be in debt"),
    ("OWN",  "Possess something"),
    ("PAD",  "Flat cushion or notepad"),
    ("PAL",  "Close friend"),
    ("PAW",  "Animal's foot"),
    ("PAY",  "Give money"),
    ("PEN",  "Writing instrument"),
    ("PET",  "Domestic animal"),
    ("PIE",  "Baked pastry dish"),
    ("PIG",  "Muddy farm animal"),
    ("PIN",  "Sharp fastening device"),
    ("PUB",  "British drinking establishment"),
    ("PUN",  "Wordplay joke"),
    ("PUP",  "Young dog"),
    ("RAG",  "Torn cloth piece"),
    ("RAM",  "Male sheep"),
    ("RAW",  "Uncooked"),
    ("RAY",  "Beam of light"),
    ("RED",  "Color of fire"),
    ("ROD",  "Thin straight stick"),
    ("ROT",  "Decay or decompose"),
    ("RUM",  "Caribbean spirit"),
    ("RUN",  "Move quickly on foot"),
    ("SEA",  "Large body of salt water"),
    ("SEW",  "Join with needle and thread"),
    ("SIP",  "Drink in small amounts"),
    ("SIX",  "Number after five"),
    ("SKI",  "Glide on snow"),
    ("SKY",  "Above the clouds"),
    ("SUM",  "Total amount"),
    ("TAN",  "Brown from sun"),
    ("TAX",  "Government charge"),
    ("TEA",  "Hot brewed drink"),
    ("TEN",  "Number after nine"),
    ("TIE",  "Neckwear or a draw"),
    ("TIN",  "Metal food container"),
    ("TOE",  "Foot digit"),
    ("TOY",  "Child's plaything"),
    ("TUB",  "Large bathing container"),
    ("TUG",  "Pull sharply"),
    ("TWO",  "Number after one"),
    ("WAR",  "Armed conflict"),
    ("WET",  "Covered in water"),
    ("WIN",  "Come first in a contest"),
    ("WIT",  "Clever humor"),
    ("WOK",  "Chinese cooking pan"),
    ("YES",  "Affirmative answer"),
    ("ARCH", "Curved stone structure"),
    ("BALL", "Round sports object"),
    ("BAND", "Group of musicians"),
    ("BANK", "Place to keep money"),
    ("BARK", "Dog's sound or tree skin"),
    ("BASE", "Bottom foundation"),
    ("BATH", "Soak in a tub"),
    ("BEAN", "Small legume"),
    ("BEAT", "Strike or musical rhythm"),
    ("BEER", "Brewed hop drink"),
    ("BELT", "Waist strap"),
    ("BIRD", "Feathered flying creature"),
    ("BLUE", "Color of the sky"),
    ("BOLD", "Daring and confident"),
    ("BONE", "Part of the skeleton"),
    ("BOOK", "Bound pages to read"),
    ("BOOT", "Footwear above the ankle"),
    ("BURN", "Damage with heat"),
    ("CALL", "Telephone or shout"),
    ("CARD", "Stiff paper greeting"),
    ("CASH", "Paper money"),
    ("COAL", "Black fossil fuel"),
    ("COAT", "Outer winter clothing"),
    ("CODE", "Secret symbol system"),
    ("COLD", "Low temperature"),
    ("COOK", "Prepare food with heat"),
    ("COOL", "Slightly cold or trendy"),
    ("CORN", "Yellow grain on cob"),
    ("CURE", "Make someone well"),
    ("CUTE", "Attractively small"),
    ("DARE", "Challenge bravely"),
    ("DARK", "Without light"),
    ("DATE", "Calendar day or fruit"),
    ("DEAD", "No longer alive"),
    ("DEAL", "Agreement or arrangement"),
    ("DEEP", "Far from the surface"),
    ("DIRT", "Soil or filth"),
    ("DISH", "Plate or food course"),
    ("DROP", "Fall or small liquid amount"),
    ("DRUM", "Percussion instrument"),
    ("DUCK", "Water bird or dodge"),
    ("DUSK", "Evening twilight"),
    ("DUST", "Fine dry particles"),
    ("FARM", "Agricultural land"),
    ("FAST", "Quick or not eating"),
    ("FILL", "Make completely full"),
    ("FIRE", "Flames and heat"),
    ("FISH", "Aquatic swimming creature"),
    ("FLAG", "National symbol on pole"),
    ("FLAT", "Level surface"),
    ("FLOW", "Move smoothly"),
    ("FOOD", "What we eat"),
    ("FOOT", "Bottom of the leg"),
    ("FORK", "Eating utensil with prongs"),
    ("FOUR", "Number after three"),
    ("FREE", "At no cost"),
    ("FROG", "Amphibian that croaks"),
    ("FULL", "Completely filled"),
    ("GOLD", "Precious yellow metal"),
    ("GROW", "Get bigger over time"),
    ("HAND", "Body part with fingers"),
    ("HARD", "Not soft or easy"),
    ("HEAL", "Recover from injury"),
    ("HEAT", "Warmth or high temperature"),
    ("HEEL", "Back part of the foot"),
    ("HELP", "Give assistance"),
    ("HERO", "Brave admired person"),
    ("HIGH", "Far above ground"),
    ("HILL", "Small raised landform"),
    ("HOLD", "Grasp in hand"),
    ("HOME", "Where you live"),
    ("HORN", "Musical instrument or protrusion"),
    ("HUGE", "Extremely large"),
    ("HUNT", "Search for game"),
    ("JUMP", "Leap into the air"),
    ("KIND", "Friendly and generous"),
    ("KING", "Male ruler"),
    ("LAKE", "Inland body of water"),
    ("LAMB", "Young sheep"),
    ("LAMP", "Light-giving device"),
    ("LAND", "Ground or arrive"),
    ("LAST", "Final or most recent"),
    ("LEAF", "Plant's flat green part"),
    ("LEFT", "Opposite of right"),
    ("LIFT", "Raise upward"),
    ("LIME", "Green citrus fruit"),
    ("LION", "King of the jungle"),
    ("LOCK", "Secure with a key"),
    ("LONG", "Extended in length"),
    ("LOVE", "Deep affection"),
    ("LUCK", "Good fortune"),
    ("LUNG", "Breathing organ"),
    ("MALE", "Opposite of female"),
    ("MASK", "Face covering"),
    ("MAZE", "Puzzle of paths"),
    ("MEAL", "Food eaten at one time"),
    ("MEAT", "Animal flesh as food"),
    ("MELT", "Turn solid to liquid"),
    ("MILK", "White dairy drink"),
    ("MIND", "Thinking organ"),
    ("MINT", "Fresh herb or make coins"),
    ("MOON", "Earth's natural satellite"),
    ("MORE", "Greater in quantity"),
    ("MOVE", "Change position"),
    ("MYTH", "Ancient traditional story"),
    ("NAIL", "Metal fastener or fingertip"),
    ("NAME", "What you call something"),
    ("NECK", "Between head and shoulders"),
    ("NICE", "Pleasant or agreeable"),
    ("NINE", "Number after eight"),
    ("NOON", "Middle of the day"),
    ("NOSE", "Organ for smelling"),
    ("NOTE", "Short written message"),
    ("ONCE", "One single time"),
    ("OPEN", "Not closed"),
    ("OVAL", "Egg-shaped"),
    ("OVEN", "Cooking appliance"),
    ("PACK", "Bundle or fill tightly"),
    ("PAGE", "Side of a book leaf"),
    ("PALE", "Light in color"),
    ("PARK", "Green outdoor space"),
    ("PART", "Section of a whole"),
    ("PATH", "Track to walk on"),
    ("PEAK", "Top of a mountain"),
    ("PEST", "Annoying creature"),
    ("PICK", "Choose or pluck"),
    ("PINE", "Evergreen tree"),
    ("PINK", "Light red color"),
    ("PIPE", "Hollow tube"),
    ("PLOT", "Plan or story outline"),
    ("PLUM", "Purple stone fruit"),
    ("POEM", "Written verse"),
    ("POOL", "Still water area"),
    ("POOR", "Having little money"),
    ("RACE", "Speed competition"),
    ("RAIN", "Water falling from clouds"),
    ("RANK", "Position in order"),
    ("RARE", "Not common"),
    ("REAL", "Actually existing"),
    ("REEF", "Underwater rock ridge"),
    ("RENT", "Pay for temporary use"),
    ("REST", "Relax or remainder"),
    ("RICE", "Staple grain"),
    ("RICH", "Having lots of money"),
    ("RIDE", "Travel on or in"),
    ("RING", "Circle or jewelry"),
    ("RISE", "Go upward"),
    ("RISK", "Chance of danger"),
    ("ROAR", "Loud animal sound"),
    ("ROCK", "Stone or music genre"),
    ("ROLE", "Part played in something"),
    ("ROOF", "Top of a building"),
    ("ROOM", "Space inside a building"),
    ("ROOT", "Plant underground part"),
    ("ROPE", "Thick twisted cord"),
    ("ROSE", "Common flowering plant"),
    ("RULE", "Regulation or govern"),
    ("RUSH", "Move very quickly"),
    ("RUST", "Orange metal corrosion"),
    ("SAFE", "Not in danger"),
    ("SAIL", "Travel by wind power"),
    ("SALT", "White flavoring mineral"),
    ("SAND", "Tiny rock granules"),
    ("SEAL", "Arctic mammal or close tight"),
    ("SEAT", "Place to sit"),
    ("SHIP", "Large ocean vessel"),
    ("SHOE", "Foot covering"),
    ("SHOP", "Retail store"),
    ("SHOW", "Display or performance"),
    ("SHUT", "Close completely"),
    ("SILK", "Smooth luxury fabric"),
    ("SING", "Make music with voice"),
    ("SINK", "Basin or go under water"),
    ("SLOW", "Not fast"),
    ("SNOW", "Frozen white precipitation"),
    ("SOCK", "Foot covering worn inside shoe"),
    ("SOFT", "Not hard"),
    ("SOIL", "Earth for growing plants"),
    ("SONG", "Musical composition"),
    ("SOUL", "Spiritual inner self"),
    ("SOUP", "Liquid food"),
    ("SPOT", "Small mark or location"),
    ("STAR", "Distant burning ball of gas"),
    ("STAY", "Remain in place"),
    ("STEM", "Plant stalk"),
    ("STEP", "Single footfall"),
    ("STEW", "Slow-cooked dish"),
    ("STOP", "Come to a halt"),
    ("SWAN", "Large white water bird"),
    ("SWIM", "Move through water"),
    ("TAIL", "Rear appendage of animal"),
    ("TALE", "Short story"),
    ("TALL", "Of great height"),
    ("TAME", "Not wild"),
    ("TASK", "Piece of work"),
    ("TEAM", "Group working together"),
    ("TENT", "Portable camping shelter"),
    ("TEST", "Trial or examination"),
    ("THIN", "Not thick"),
    ("TIME", "Duration or clock reading"),
    ("TINY", "Extremely small"),
    ("TOAD", "Warty amphibian"),
    ("TOOL", "Implement for work"),
    ("TOUR", "Journey or visit"),
    ("TOWN", "Smaller than a city"),
    ("TRIM", "Cut neatly"),
    ("TRIP", "Journey or stumble"),
    ("TUBE", "Hollow cylinder"),
    ("TUNE", "Musical melody"),
    ("TURN", "Rotate or change direction"),
    ("TWIN", "One of two identical siblings"),
    ("VINE", "Climbing plant"),
    ("VOTE", "Express a preference"),
    ("WAKE", "Stop sleeping"),
    ("WALK", "Move on foot"),
    ("WALL", "Vertical dividing surface"),
    ("WARM", "Moderately hot"),
    ("WASH", "Clean with water"),
    ("WAVE", "Water movement or gesture"),
    ("WEAR", "Have on your body"),
    ("WEED", "Unwanted garden plant"),
    ("WINE", "Fermented grape drink"),
    ("WING", "Bird's flying limb"),
    ("WIRE", "Thin metal strand"),
    ("WISH", "Desire or hope"),
    ("WOLF", "Wild canine"),
    ("WOOD", "Hard tree material"),
    ("WOOL", "Sheep's coat fiber"),
    ("WORD", "Unit of language"),
    ("WORK", "Exertion for a purpose"),
    ("WORM", "Legless burrowing creature"),
    ("YELL", "Shout loudly"),
    ("ZERO", "Nothing or the number 0"),
    ("ZONE", "Designated area"),
    ("BREAD", "Baked staple food"),
    ("CHAIR", "Seat with back and legs"),
    ("CLEAN", "Free from dirt"),
    ("CLEAR", "Transparent or obvious"),
    ("CLOCK", "Time-keeping device"),
    ("CLOUD", "Fluffy mass in the sky"),
    ("CREAM", "Thick dairy product"),
    ("CROWN", "Royal headwear"),
    ("DANCE", "Move rhythmically to music"),
    ("DRAFT", "First version or air current"),
    ("DRAIN", "Remove liquid from"),
    ("DREAM", "Sleeping vision or hope"),
    ("DRINK", "Consume liquid"),
    ("EAGLE", "Large bird of prey"),
    ("EARLY", "Before expected time"),
    ("EIGHT", "Number after seven"),
    ("FENCE", "Boundary barrier"),
    ("FIELD", "Open area of land"),
    ("FLOAT", "Rest on surface of water"),
    ("FLOOR", "Bottom surface of a room"),
    ("FLOUR", "Ground grain powder"),
    ("FRESH", "New or not stale"),
    ("FRUIT", "Sweet plant produce"),
    ("GLASS", "Transparent brittle material"),
    ("GLOVE", "Hand covering"),
    ("GRACE", "Elegant movement"),
    ("GRAIN", "Cereal crop seed"),
    ("GRASS", "Green ground cover"),
    ("GREAT", "Very large or impressive"),
    ("GREEN", "Color of grass"),
    ("HAPPY", "Feeling pleasure"),
    ("HEART", "Organ that pumps blood"),
    ("HORSE", "Large riding animal"),
    ("HOUSE", "Building to live in"),
    ("JUICE", "Liquid squeezed from fruit"),
    ("KNIFE", "Sharp cutting blade"),
    ("LARGE", "Bigger than average"),
    ("LAUGH", "Express amusement vocally"),
    ("LAYER", "Flat thickness of material"),
    ("LEARN", "Gain new knowledge"),
    ("LIGHT", "Visible radiation or not heavy"),
    ("LUCKY", "Having good fortune"),
    ("LUNCH", "Midday meal"),
    ("MAGIC", "Mysterious power"),
    ("MATCH", "Competition or igniting stick"),
    ("MONEY", "Currency for exchange"),
    ("MONTH", "One of twelve calendar periods"),
    ("MOUSE", "Small rodent"),
    ("MOUTH", "Opening for eating and speaking"),
    ("MUSIC", "Organized sound"),
    ("NIGHT", "Dark hours after sunset"),
    ("NURSE", "Medical care professional"),
    ("OCEAN", "Vast body of salt water"),
    ("OLIVE", "Small salty Mediterranean fruit"),
    ("PAPER", "Thin writing material"),
    ("PEACE", "Absence of conflict"),
    ("PEACH", "Fuzzy soft stone fruit"),
    ("PEARL", "Gem formed inside oysters"),
    ("PHONE", "Communication device"),
    ("PIANO", "Large keyboard instrument"),
    ("PILOT", "Person who flies aircraft"),
    ("PIZZA", "Italian baked flatbread dish"),
    ("PLACE", "A specific location"),
    ("PLAIN", "Simple or flat open land"),
    ("PLANE", "Aircraft or flat surface"),
    ("PLANT", "Living organism that grows"),
    ("PLATE", "Flat dish for food"),
    ("POINT", "Sharp tip or location"),
    ("POUND", "Unit of weight or hit hard"),
    ("POWER", "Strength or electricity"),
    ("PRESS", "Push firmly or news media"),
    ("PRICE", "Cost of something"),
    ("PRIDE", "Feeling of self-worth"),
    ("PRINT", "Reproduce text on paper"),
    ("PRIZE", "Reward for winning"),
    ("PUNCH", "Strike with fist or drink"),
    ("QUEEN", "Female ruler or chess piece"),
    ("QUICK", "Moving fast"),
    ("QUIET", "Making little noise"),
    ("REACH", "Extend to get something"),
    ("READY", "Fully prepared"),
    ("RIGHT", "Correct or opposite of left"),
    ("RIVER", "Large natural water flow"),
    ("ROUND", "Circular or a series"),
    ("ROUTE", "Path taken to destination"),
    ("ROYAL", "Relating to a king or queen"),
    ("RULER", "Measuring stick or leader"),
    ("SAUCE", "Liquid condiment"),
    ("SCALE", "Measure weight or fish covering"),
    ("SCENE", "Setting or view"),
    ("SCOUT", "Explore ahead"),
    ("SHADE", "Cool dark area"),
    ("SHAKE", "Move rapidly back and forth"),
    ("SHAPE", "Outer form of something"),
    ("SHARE", "Give portion to others"),
    ("SHARK", "Large ocean predator"),
    ("SHARP", "Having a fine edge"),
    ("SHEET", "Flat fabric for bed"),
    ("SHELF", "Horizontal storage board"),
    ("SHELL", "Hard outer casing"),
    ("SHIRT", "Upper body garment"),
    ("SHORT", "Not tall or long"),
    ("SHOUT", "Call out loudly"),
    ("SIGHT", "The ability to see"),
    ("SKILL", "Learned ability"),
    ("SLEEP", "Rest with eyes closed"),
    ("SLICE", "Thin flat piece cut off"),
    ("SLOPE", "Inclined surface"),
    ("SMART", "Intelligent or stylish"),
    ("SMELL", "Detect odor with nose"),
    ("SMILE", "Happy facial expression"),
    ("SMOKE", "Visible gas from fire"),
    ("SNAIL", "Slow shell-bearing mollusc"),
    ("SNAKE", "Legless reptile"),
    ("SOLID", "Firm and stable"),
    ("SPACE", "Empty area or outer universe"),
    ("SPARE", "Extra reserve item"),
    ("SPEAK", "Express with words"),
    ("SPICE", "Flavoring from plants"),
    ("SPOON", "Utensil for liquids"),
    ("SPORT", "Physical game or activity"),
    ("SPRAY", "Scatter liquid in droplets"),
    ("STACK", "Pile of things on top"),
    ("STAGE", "Raised platform for performers"),
    ("STAND", "Be upright on feet"),
    ("STARE", "Look fixedly at"),
    ("START", "Begin something"),
    ("STEAM", "Hot water vapor"),
    ("STEEL", "Strong iron alloy"),
    ("STICK", "Thin piece of wood"),
    ("STILL", "Not moving"),
    ("STONE", "Hard mineral rock"),
    ("STORM", "Violent weather"),
    ("STRAW", "Drinking tube or dried grass"),
    ("STUDY", "Learn a subject"),
    ("STYLE", "Distinctive manner"),
    ("SUGAR", "Sweet crystalline substance"),
    ("SWEET", "Tasting like sugar"),
    ("SWIFT", "Moving very fast"),
    ("SWORD", "Long bladed weapon"),
    ("TABLE", "Flat-topped furniture"),
    ("TASTE", "Sense food with tongue"),
    ("TEACH", "Instruct or educate"),
    ("TEETH", "Biting structures in mouth"),
    ("THICK", "Not thin"),
    ("THINK", "Use your mind"),
    ("THROW", "Propel through the air"),
    ("THUMB", "Shortest finger"),
    ("TODAY", "The present day"),
    ("TOTAL", "Complete sum"),
    ("TOUCH", "Make contact with"),
    ("TOUGH", "Strong and resilient"),
    ("TOWEL", "Cloth for drying"),
    ("TRACE", "Follow the path of"),
    ("TRACK", "Path or follow movement"),
    ("TRADE", "Exchange goods"),
    ("TRAIL", "Rough path through nature"),
    ("TRAIN", "Rail vehicle or practice"),
    ("TRASH", "Waste or rubbish"),
    ("TREAT", "Something enjoyable or handle"),
    ("TREND", "Current fashion or direction"),
    ("TRUST", "Believe in reliability"),
    ("TRUTH", "What is actually true"),
    ("TULIP", "Cup-shaped spring flower"),
    ("TWIST", "Turn and bend"),
    ("UNTIL", "Up to a certain time"),
    ("UPPER", "Higher of two things"),
    ("VALID", "Sound and defensible"),
    ("VALUE", "Worth or importance"),
    ("VERSE", "Lines of poetry"),
    ("VISIT", "Go to see someone"),
    ("VITAL", "Absolutely essential"),
    ("VIVID", "Bright and intense"),
    ("VOICE", "Sound produced when speaking"),
    ("WATCH", "Look at or wrist timepiece"),
    ("WATER", "Liquid we drink"),
    ("WHALE", "Largest ocean mammal"),
    ("WHEAT", "Cereal grain for bread"),
    ("WHEEL", "Circular rotating object"),
    ("WHITE", "Color of snow"),
    ("WHOLE", "Complete and entire"),
    ("WOMAN", "Adult female"),
    ("WORLD", "Planet Earth or society"),
    ("WORRY", "Feel anxious"),
    ("WORTH", "Monetary or intrinsic value"),
    ("WOULD", "Expressing conditional"),
    ("YOUTH", "Period of being young"),
    ("YIELD", "Produce or give way"),
],

"Medium": [
    ("TIGER",  "Striped big cat"),
    ("PRISM",  "Splits light into spectrum"),
    ("FLAME",  "Fire's visible part"),
    ("GROVE",  "Small group of trees"),
    ("CRANE",  "Tall construction machine"),
    ("BLEND",  "Mix together smoothly"),
    ("CHEST",  "Torso or storage box"),
    ("DRIFT",  "Move slowly without direction"),
    ("ELDER",  "Older or senior person"),
    ("FLOCK",  "Group of birds"),
    ("GLOBE",  "Spherical world model"),
    ("HATCH",  "Small door or to plan secretly"),
    ("INERT",  "Chemically inactive"),
    ("JEWEL",  "Precious stone"),
    ("KNACK",  "Special talent or skill"),
    ("LUNAR",  "Relating to the moon"),
    ("MAPLE",  "Tree that produces syrup"),
    ("NERVE",  "Fiber that transmits signals"),
    ("OPERA",  "Dramatic musical performance"),
    ("PLUMB",  "Perfectly vertical"),
    ("QUERY",  "A question"),
    ("RAVEN",  "Large black bird"),
    ("SWAMP",  "Marshy wetland"),
    ("TORCH",  "Handheld light source"),
    ("ULCER",  "Stomach sore"),
    ("VENOM",  "Poisonous secretion"),
    ("WALTZ",  "Three-beat ballroom dance"),
    ("XYLEM",  "Plant water-transport tissue"),
    ("YACHT",  "Luxury sailing vessel"),
    ("ZEBRA",  "Black and white striped animal"),
    ("AGILE",  "Able to move quickly"),
    ("BEACH",  "Sandy shore"),
    ("CLAMP",  "Device that holds things"),
    ("DEPOT",  "Storage or transit hub"),
    ("EPOCH",  "Period of history"),
    ("FABLE",  "Short moral story"),
    ("GAUZE",  "Light transparent fabric"),
    ("HAVEN",  "Safe place"),
    ("INDEX",  "Alphabetical reference list"),
    ("JOUST",  "Medieval lance combat"),
    ("KNELT",  "Past tense of kneel"),
    ("LATCH",  "Door fastening"),
    ("MANOR",  "Large country house"),
    ("NINJA",  "Covert Japanese warrior"),
    ("ONION",  "Layered vegetable that causes tears"),
    ("PANEL",  "Flat section or group of experts"),
    ("QUOTA",  "Required amount"),
    ("RIDGE",  "Narrow raised strip"),
    ("SCONE",  "British baked treat"),
    ("TABOO",  "Culturally forbidden"),
    ("USURP",  "Seize power illegally"),
    ("VIGIL",  "Watchful waiting period"),
    ("WHIRL",  "Spin rapidly"),
    ("AXIOM",  "Self-evident truth"),
    ("BRAWL",  "Rough fight"),
    ("CALYX",  "Outer leaf of flower"),
    ("DECOY",  "Lure to mislead"),
    ("ENVOY",  "Diplomatic messenger"),
    ("FJORD",  "Narrow coastal inlet"),
    ("GLYPH",  "Carved symbol"),
    ("HYDRA",  "Multi-headed mythical creature"),
    ("ICHOR",  "Fluid in gods' veins"),
    ("JUNTA",  "Military ruling group"),
    ("KARMA",  "Cause and effect principle"),
    ("LLAMA",  "South American pack animal"),
    ("MAXIM",  "General truth or rule"),
    ("NEXUS",  "Connection or link"),
    ("OZONE",  "Atmospheric gas layer"),
    ("PIVOT",  "Central turning point"),
    ("QUAFF",  "Drink heartily"),
    ("REALM",  "Kingdom or domain"),
    ("SQUAB",  "Young pigeon"),
    ("TRYST",  "Secret romantic meeting"),
    ("UNIFY",  "Bring together as one"),
    ("VAGUE",  "Not clearly defined"),
    ("WRATH",  "Intense anger"),
    ("ABBOT",  "Head of a monastery"),
    ("BROTH",  "Thin soup or stock"),
    ("CHASM",  "Deep crack in earth"),
    ("DELTA",  "River mouth or Greek letter"),
    ("EMBER",  "Glowing fire remains"),
    ("FROND",  "Fern or palm leaf"),
    ("GUILE",  "Clever deception"),
    ("HELIX",  "Spiral shape like DNA"),
    ("ICING",  "Sweet cake topping"),
    ("JOKER",  "Comedian or wild card"),
    ("LAPEL",  "Folded coat collar flap"),
    ("MOOSE",  "Largest deer species"),
    ("NYMPH",  "Minor nature goddess"),
    ("OXIDE",  "Compound with oxygen"),
    ("PIXEL",  "Smallest screen element"),
    ("QUILL",  "Feather used as pen"),
    ("RIVET",  "Metal fastening pin"),
    ("SALVO",  "Simultaneous gunfire"),
    ("TIDAL",  "Relating to ocean tides"),
    # ── Extra Medium words ──
    ("ABYSS",  "Bottomless chasm"),
    ("ACORN",  "Oak tree's seed"),
    ("ADORN",  "Decorate with ornaments"),
    ("AGONY",  "Extreme suffering"),
    ("ALGAE",  "Aquatic plant-like organisms"),
    ("ALOFT",  "Up in the air"),
    ("ALOOF",  "Distant and reserved"),
    ("AMBLE",  "Walk at a leisurely pace"),
    ("AMEND",  "Make changes to improve"),
    ("AMPLE",  "More than enough"),
    ("ANNEX",  "Add territory or extension"),
    ("APRON",  "Kitchen protective garment"),
    ("ARDOR",  "Passionate enthusiasm"),
    ("ATOLL",  "Ring-shaped coral island"),
    ("AUDIT",  "Official financial examination"),
    ("AUGUR",  "Predict from signs"),
    ("AVAIL",  "Be of use or benefit"),
    ("AVERT",  "Prevent or turn away"),
    ("BABEL",  "Confused noisy situation"),
    ("BEVEL",  "Sloped cut or edge"),
    ("BOGUS",  "Not genuine or fake"),
    ("BRASH",  "Self-assertive in rude way"),
    ("BRINE",  "Salt water solution"),
    ("BRISK",  "Active and energetic"),
    ("BROIL",  "Cook under direct heat"),
    ("BROOK",  "Small natural stream"),
    ("BRUNT",  "Worst part of impact"),
    ("BURLY",  "Large and sturdy build"),
    ("CACHE",  "Hidden store of items"),
    ("CAPER",  "Frolic or pickled flower bud"),
    ("CARGO",  "Goods carried by ship"),
    ("CARVE",  "Cut into a shape"),
    ("CHAFE",  "Irritate by rubbing"),
    ("CHARM",  "Attract or delight"),
    ("CHASE",  "Pursue rapidly"),
    ("CHIDE",  "Scold mildly"),
    ("CHORD",  "Musical notes played together"),
    ("CIVIL",  "Relating to citizens"),
    ("CLEFT",  "Split into two parts"),
    ("CLING",  "Hold tightly to"),
    ("COMET",  "Icy body orbiting the sun"),
    ("COMIC",  "Funny or comedian"),
    ("COVET",  "Yearn to possess"),
    ("COWER",  "Crouch in fear"),
    ("CRAFT",  "Skill or handmade object"),
    ("CREAK",  "Make a harsh squeak"),
    ("CREED",  "Set of beliefs"),
    ("CREST",  "Top of a wave or hill"),
    ("CRISP",  "Firm and brittle"),
    ("CRUDE",  "Rough or unrefined"),
    ("CRUEL",  "Causing pain willingly"),
    ("CRUST",  "Hard outer layer"),
    ("CRYPT",  "Underground burial chamber"),
    ("CURSE",  "Wish evil upon someone"),
    ("DEBUT",  "First public appearance"),
    ("DECOR",  "Interior style and furnishing"),
    ("DEFER",  "Postpone or yield to"),
    ("DENSE",  "Tightly packed together"),
    ("DETOX",  "Remove harmful substances"),
    ("DEXTR",  "Skill with the hands"),
    ("DODGY",  "Dishonest or risky"),
    ("DOUSE",  "Drench with water"),
    ("DOWRY",  "Property brought by bride"),
    ("DUVET",  "Thick quilted bed cover"),
    ("DWARF",  "Very small person or star"),
    ("EASEL",  "Artist's canvas stand"),
    ("EERIE",  "Strange and frightening"),
    ("ELBOW",  "Joint between arm segments"),
    ("ELUDE",  "Escape from cleverly"),
    ("EMOTE",  "Express emotion dramatically"),
    ("ENDOW",  "Provide with quality or gift"),
    ("ETHOS",  "Character of a group"),
    ("EVADE",  "Escape or avoid cleverly"),
    ("EXACT",  "Perfectly accurate"),
    ("EXERT",  "Apply effort or force"),
    ("EXPEL",  "Force out officially"),
    ("EXUDE",  "Ooze or radiate strongly"),
    ("FAINT",  "Lose consciousness briefly"),
    ("FATAL",  "Causing death"),
    ("FEIGN",  "Pretend to have quality"),
    ("FELON",  "Person guilty of serious crime"),
    ("FERVENT","Intensely passionate"),
    ("FETCH",  "Go and get something"),
    ("FEUD",   "Prolonged bitter conflict"),
    ("FIEND",  "Very wicked person"),
    ("FLAIR",  "Natural talent or style"),
    ("FLANK",  "Side of body or military wing"),
    ("FLAUNT", "Display ostentatiously"),
    ("FLEET",  "Group of ships or vehicles"),
    ("FLESH",  "Soft tissue of body"),
    ("FLINT",  "Hard rock for fire-starting"),
    ("FLUKE",  "Unlikely lucky event"),
    ("FLURRY", "Brief spell of activity"),
    ("FORAY",  "Sudden attack or venture"),
    ("FORGE",  "Create metal or fake"),
    ("FORTE",  "One's strong point"),
    ("FORUM",  "Public discussion place"),
    ("FRAIL",  "Weak and delicate"),
    ("FRAUD",  "Criminal deception"),
    ("FREAK",  "Unusual or obsessed person"),
    ("FRIAR",  "Member of religious order"),
    ("FROST",  "Thin ice crystals formed"),
    ("FRUGAL", "Economical with resources"),
    ("FUNGI",  "Kingdom including mushrooms"),
    ("GAUDY",  "Tastelessly showy"),
    ("GAVEL",  "Judge's small mallet"),
    ("GAWKY",  "Awkward and ungainly"),
    ("GIDDY",  "Dizzy or excitedly silly"),
    ("GIRTH",  "Measurement around something"),
    ("GLARE",  "Stare angrily or bright light"),
    ("GLEAN",  "Gather gradually"),
    ("GLEAM",  "Shine with soft light"),
    ("GLOOM",  "Darkness or sadness"),
    ("GLOSS",  "Shiny surface or explanation"),
    ("GRAFT",  "Hard work or corrupt gain"),
    ("GRASP",  "Seize firmly or understand"),
    ("GRAZE",  "Feed on grass or scrape"),
    ("GREED",  "Intense desire for more"),
    ("GREET",  "Welcome or acknowledge"),
    ("GRIEF",  "Deep sorrow"),
    ("GRILL",  "Cook on metal bars"),
    ("GRIMY",  "Covered in grime"),
    ("GRIPE",  "Complain persistently"),
    ("GROAN",  "Low sound of pain"),
    ("GROPE",  "Feel about blindly"),
    ("GROSS",  "Disgusting or total before deductions"),
    ("GROWL",  "Low threatening sound"),
    ("GRUFF",  "Rough or stern in manner"),
    ("GUISE",  "Outward appearance"),
    ("GULCH",  "Narrow rocky ravine"),
    ("GUSTO",  "Enthusiasm and energy"),
    ("HARDY",  "Robust and capable of enduring"),
    ("HARSH",  "Unpleasantly rough"),
    ("HASTE",  "Excessive speed"),
    ("HAUNT",  "Appear or visit repeatedly"),
    ("HAVOC",  "Widespread destruction"),
    ("HAZARD", "Danger or risk"),
    ("HEFTY",  "Large and heavy"),
    ("HENCE",  "Therefore or from here"),
    ("HOARD",  "Hidden stockpile"),
    ("HOIST",  "Raise or lift up"),
    ("HONOR",  "High respect or integrity"),
    ("HOWL",   "Long loud cry"),
    ("HULK",   "Large heavy person or ship"),
    ("HUMID",  "Damp and warm"),
    ("HYENA",  "African scavenging mammal"),
    ("IDYLL",  "Peaceful rural scene"),
    ("IMPEL",  "Drive forward or urge"),
    ("IMPLY",  "Suggest without stating"),
    ("INANE",  "Lacking sense or meaning"),
    ("INCUR",  "Become subject to something"),
    ("INEPT",  "Having no skill"),
    ("INFER",  "Conclude from evidence"),
    ("INGOT",  "Block of cast metal"),
    ("INNER",  "Inside or internal"),
    ("INPUT",  "What is put in"),
    ("INTER",  "Bury a corpse"),
    ("INTRO",  "Short opening section"),
    ("INURE",  "Accustom to hardship"),
    ("IRATE",  "Feeling intense anger"),
    ("JAUNT",  "Short pleasure trip"),
    ("JAGGED", "With sharp uneven points"),
    ("KNAVE",  "Dishonest person or jack card"),
    ("KNEEL",  "Rest on bent knees"),
    ("LAPSE",  "Brief failure or interval"),
    ("LARVA",  "Immature insect form"),
    ("LEACH",  "Drain away gradually"),
    ("LEDGE",  "Narrow horizontal shelf"),
    ("LEERY",  "Cautious and suspicious"),
    ("LIBEL",  "Published false statement"),
    ("LOFTY",  "Very high or noble"),
    ("LUNGE",  "Sudden forward thrust"),
    ("LUSTY",  "Healthy and vigorous"),
    ("MALICE", "Desire to harm others"),
    ("MANIC",  "Showing wild excitement"),
    ("MIRTH",  "Great amusement"),
    ("MOURN",  "Feel grief after loss"),
    ("MURKY",  "Dark and gloomy"),
    ("NADIR",  "Lowest point of something"),
    ("NIECE",  "Brother's or sister's daughter"),
    ("NOBLE",  "Having high moral qualities"),
    ("NOTCH",  "V-shaped cut or level"),
    ("NOVEL",  "New and original or book"),
    ("NUDGE",  "Push gently with elbow"),
    ("NURSE",  "Care for the sick"),
    ("OBLIQUE","Neither parallel nor perpendicular"),
    ("ODIUM",  "General hatred"),
    ("OFFHAND","Without previous thought"),
    ("ONSET",  "Beginning of something"),
    ("OPAQUE", "Not transparent"),
    ("ORACLE", "Source of wise counsel"),
    ("ORBIT",  "Curved path around body"),
    ("ORDEAL", "Painful difficult experience"),
    ("OUNCE",  "Small unit of weight"),
    ("OUGHT",  "Used to express duty"),
    ("OUTDO",  "Be more successful than"),
    ("OUTWIT", "Defeat by being clever"),
    ("PARCH",  "Make dry through heat"),
    ("PARKA",  "Hooded waterproof jacket"),
    ("PARSE",  "Analyze grammatically"),
    ("PATIO",  "Outdoor paved area"),
    ("PAUPER", "Very poor person"),
    ("PENCE",  "British plural of penny"),
    ("PERCH",  "Rest on narrow surface"),
    ("PERJURE","Lie under oath"),
    ("PETTY",  "Of little importance"),
    ("PIQUE",  "Stimulate interest or annoy"),
    ("PLAID",  "Checkered pattern fabric"),
    ("PLIGHT", "Difficult situation"),
    ("PLUCK",  "Pick or pull off"),
    ("PLUME",  "Long decorative feather"),
    ("POACH",  "Cook gently or hunt illegally"),
    ("PODIUM", "Raised speaking platform"),
    ("POISE",  "Graceful balance"),
    ("POUCH",  "Small flexible bag"),
    ("PRANK",  "Playful trick"),
    ("PREEN",  "Tidy feathers or appearance"),
    ("PRIMAL", "Relating to early stage"),
    ("PRIVY",  "Sharing secret knowledge"),
    ("PROBE",  "Investigate thoroughly"),
    ("PRONE",  "Likely to or lying face down"),
    ("PRUNE",  "Dried plum or trim plant"),
    ("PSALM",  "Sacred song or hymn"),
    ("PULSE",  "Regular heartbeat or legume"),
    ("QUALM",  "Feeling of doubt or scruple"),
    ("QUIRK",  "Peculiar habit or trait"),
    ("REBUT",  "Prove wrong with evidence"),
    ("REEDY",  "Thin and weak sounding"),
    ("REGAL",  "Relating to royalty"),
    ("REIGN",  "Period of rule"),
    ("RELAX",  "Become less tense"),
    ("REMIT",  "Send money or cancel"),
    ("RENEW",  "Resume after pause"),
    ("REPEL",  "Drive away or disgust"),
    ("REPUTE", "General opinion of someone"),
    ("RESIN",  "Sticky plant substance"),
    ("REVEL",  "Enjoy lively celebration"),
    ("RIGID",  "Stiff and not flexible"),
    ("RIPEN",  "Become mature or ready"),
    ("RISKY",  "Involving chance of harm"),
    ("RIVAL",  "Person competing with another"),
    ("ROBIN",  "Small red-breasted bird"),
    ("ROCKY",  "Covered with rocks"),
    ("ROUGE",  "Red cosmetic powder"),
    ("ROUGH",  "Not smooth or gentle"),
    ("ROWDY",  "Noisy and disorderly"),
    ("RUGBY",  "Full-contact team ball sport"),
    ("RURAL",  "Relating to countryside"),
    ("RUSTLE", "Make soft crackling sound"),
    ("SCAMP",  "Mischievous person"),
    ("SCANT",  "Barely sufficient"),
    ("SCOFF",  "Mock or eat hastily"),
    ("SCORCH", "Burn surface of"),
    ("SCOUR",  "Clean by hard rubbing"),
    ("SCOUT",  "Search area or advance spy"),
    ("SCOWL",  "Frown with disapproval"),
    ("SCRAWL", "Write untidily"),
    ("SCRUB",  "Clean by hard rubbing"),
    ("SEIZE",  "Take hold of suddenly"),
    ("SERENE", "Calm and peaceful"),
    ("SHEEN",  "Soft luster on surface"),
    ("SKIRT",  "Go around edge of"),
    ("SLACK",  "Not tight or busy"),
    ("SLANT",  "Slope in direction"),
    ("SLOTH",  "Laziness or slow mammal"),
    ("SMEAR",  "Spread over surface"),
    ("SMITE",  "Strike with great force"),
    ("SNARE",  "Trap for animals"),
    ("SNEAK",  "Move quietly and secretly"),
    ("SNEER",  "Contemptuous smile"),
    ("SNIDE",  "Derogatory in manner"),
    ("SNIFF",  "Inhale through nose"),
    ("SNOOP",  "Pry into others' affairs"),
    ("SNORE",  "Breathe noisily in sleep"),
    ("SODDEN", "Saturated with water"),
    ("SPAWN",  "Produce offspring"),
    ("SPECK",  "Tiny spot or particle"),
    ("SPIRE",  "Tall pointed church tower"),
    ("SPUNK",  "Courage and determination"),
    ("SPURN",  "Reject with contempt"),
    ("STAIN",  "Mark with color"),
    ("STALE",  "No longer fresh"),
    ("STALK",  "Stem or follow secretly"),
    ("STALL",  "Delay or stop functioning"),
    ("STARK",  "Bare and harsh"),
    ("STARVE", "Suffer extreme hunger"),
    ("STINGY", "Unwilling to spend"),
    ("STOMP",  "Tread heavily"),
    ("STRAP",  "Long flat strip"),
    ("STRAY",  "Move away from group"),
    ("STRIFE", "Angry or bitter disagreement"),
    ("STRIP",  "Remove covering or narrow piece"),
    ("STROLL", "Walk in leisurely way"),
    ("STRUNG", "Past of string"),
    ("STUMP",  "Tree trunk or baffle"),
    ("STUNT",  "Daring act or restrict growth"),
    ("SUAVE",  "Charming and confident"),
    ("SULKY",  "Moody and withdrawn"),
    ("SURGE",  "Move forward suddenly"),
    ("SWATHE", "Wrap in layers"),
    ("SWEAR",  "Make solemn promise"),
    ("SWIPE",  "Strike with sweeping blow"),
    ("SWIRL",  "Move in twisting pattern"),
    ("SWOON",  "Faint from emotion"),
    ("SYRUP",  "Thick sweet liquid"),
    ("TACKY",  "Sticky or in poor taste"),
    ("TALON",  "Bird of prey's claw"),
    ("TANGO",  "Latin American ballroom dance"),
    ("TAUNT",  "Provoke with mocking words"),
    ("TAWNY",  "Brownish-yellow color"),
    ("TERSE",  "Brief and to the point"),
    ("THATCH", "Dried plant roofing material"),
    ("THWART", "Prevent from succeeding"),
    ("TINGE",  "Slight trace of color"),
    ("TIPSY",  "Slightly drunk"),
    ("TOKEN",  "Small symbolic object"),
    ("TORSO",  "Trunk of human body"),
    ("TOXIC",  "Poisonous or harmful"),
    ("TRAMP",  "Walk with heavy steps"),
    ("TREAD",  "Walk on or tire pattern"),
    ("TRUCE",  "Temporary halt of fighting"),
    ("TRUNK",  "Elephant's nose or storage box"),
    ("TUNIC",  "Loose sleeveless garment"),
    ("TURBO",  "Using exhaust-driven compressor"),
    ("TWEAK",  "Twist or adjust slightly"),
    ("TWIRL",  "Spin or rotate quickly"),
    ("TYRANT", "Cruel oppressive ruler"),
    ("ULTRA",  "Extreme degree or beyond"),
    ("UNDUE",  "Unwarranted or excessive"),
    ("UPSET",  "Make unhappy or overturn"),
    ("USHER",  "Show to seats or doorkeeper"),
    ("UTTER",  "Speak or complete"),
    ("VAUNT",  "Boast about proudly"),
    ("VERGE",  "Edge or be on point of"),
    ("VIGOR",  "Physical strength and energy"),
    ("VIXEN",  "Female fox or quarrelsome woman"),
    ("VODKA",  "Clear Eastern European spirit"),
    ("VOUCH",  "Assert truth of something"),
    ("WAVER",  "Become unsteady or hesitate"),
    ("WEARY",  "Exhausted from long effort"),
    ("WIELD",  "Handle a weapon or tool"),
    ("WISPY",  "Delicate and light"),
    ("WRING",  "Squeeze or twist"),
    ("YEARN",  "Have intense longing"),
    ("ZESTY",  "Fresh and lively"),
    ("ZONAL",  "Relating to zones"),
],

"Hard": [
    ("EPHEMERAL",   "Lasting a very short time"),
    ("LACONIC",     "Using very few words"),
    ("MELLIFLUOUS", "Sweet or musical sounding"),
    ("QUIXOTIC",    "Unrealistically idealistic"),
    ("SYCOPHANT",   "Flatterer who seeks favor"),
    ("TENACIOUS",   "Holding firm despite resistance"),
    ("UBIQUITOUS",  "Present everywhere at once"),
    ("VORACIOUS",   "Consuming large amounts eagerly"),
    ("WISTFUL",     "Longing with gentle sadness"),
    ("ZEALOUS",     "Intensely enthusiastic"),
    ("ABSTRUSE",    "Difficult to understand"),
    ("BELLICOSE",   "Ready to argue or fight"),
    ("CACOPHONY",   "Harsh discordant mixture of sounds"),
    ("DIDACTIC",    "Intended to teach"),
    ("EQUIVOCAL",   "Open to more than one interpretation"),
    ("FASTIDIOUS",  "Very attentive to detail"),
    ("GARRULOUS",   "Excessively talkative"),
    ("HEGEMONY",    "Leadership or dominance"),
    ("IMPETUOUS",   "Acting without thinking"),
    ("JINGOISM",    "Extreme patriotism"),
    ("KOWTOW",      "Act in obsequious manner"),
    ("LOQUACIOUS",  "Tending to talk a great deal"),
    ("MALFEASANCE", "Wrongdoing by official"),
    ("NEFARIOUS",   "Wicked or criminal"),
    ("OBDURATE",    "Stubbornly refusing to change"),
    ("PERNICIOUS",  "Having harmful effect"),
    ("QUERULOUS",   "Complaining in petulant way"),
    ("RECALCITRANT","Uncooperative and obstinate"),
    ("SOLILOQUY",   "Speaking thoughts aloud alone"),
    ("TRUCULENT",   "Eager to fight or argue"),
    ("ACRIMONY",    "Bitterness or ill feeling"),
    ("BENEVOLENT",  "Well meaning and kind"),
    ("CIRCUMSPECT", "Wary and unwilling to take risks"),
    ("DELETERIOUS", "Causing harm or damage"),
    ("ENIGMATIC",   "Mysterious and difficult to understand"),
    ("FORTUITOUS",  "Happening by lucky chance"),
    ("GRANDILOQUENT","Using pompous language"),
    ("HYPERBOLE",   "Exaggerated statement"),
    ("INSCRUTABLE", "Impossible to understand"),
    ("JOCULAR",     "Fond of joking"),
    ("LANGUID",     "Weak or lacking energy"),
    ("MENDACIOUS",  "Not telling the truth"),
    ("NASCENT",     "Just coming into existence"),
    ("OBSEQUIOUS",  "Overly eager to serve"),
    ("PARSIMONIOUS","Excessively frugal"),
    ("RANCOROUS",   "Having bitter resentment"),
    ("SAGACIOUS",   "Having good judgment"),
    ("TACITURN",    "Habitually silent"),
    ("UNCTUOUS",    "Excessively flattering"),
    ("VACUOUS",     "Lacking intelligence"),
    ("WINSOME",     "Attractive or appealing"),
    ("ACUMEN",      "Ability to make good judgments"),
    ("BRAZEN",      "Bold and without shame"),
    ("COGENT",      "Clear and convincing"),
    ("DEARTH",      "Scarcity or lack of something"),
    ("ERSATZ",      "Made as inferior substitute"),
    ("FURTIVE",     "Attempting to avoid notice"),
    ("GNARLY",      "Difficult or unpleasant"),
    ("HUBRIS",      "Excessive pride or confidence"),
    ("IMBUE",       "Inspire or pervade with feeling"),
    ("JARGON",      "Special words of a profession"),
    ("KITSCH",      "Art considered tacky"),
    ("LUCID",       "Clear and easy to understand"),
    ("MYOPIC",      "Lacking imagination or foresight"),
    ("NUANCE",      "Subtle difference in meaning"),
    ("OBTUSE",      "Slow to understand"),
    ("PEDANTIC",    "Overly concerned with detail"),
    ("RAMPANT",     "Spreading unchecked"),
    ("SCATHING",    "Witheringly critical"),
    ("TERSE",       "Brief and to the point"),
    ("UMBRAGE",     "Offense or annoyance"),
    ("VAPID",       "Offering nothing stimulating"),
    ("WANTON",      "Deliberate and unprovoked"),
    ("ACERBIC",     "Sharp and forthright"),
    ("BLITHE",      "Showing casual indifference"),
    ("CALLOW",      "Inexperienced and immature"),
    ("DIATRIBE",    "Forceful bitter criticism"),
    ("ERUDITE",     "Having wide knowledge"),
    ("FATUOUS",     "Silly and pointless"),
    ("GERMANE",     "Relevant to the subject"),
    ("HAPLESS",     "Unlucky"),
    ("INIMICAL",    "Tending to obstruct or harm"),
    ("JAUNDICE",    "Yellowing of skin or bias"),
    ("KINETIC",     "Relating to motion"),
    ("LISTLESS",    "Lacking energy or enthusiasm"),
    ("MAUDLIN",     "Self-pityingly sentimental"),
    ("NEBULOUS",    "In the form of a cloud"),
    ("OFFICIOUS",   "Assertive of authority"),
    ("PITHY",       "Concise and powerfully expressive"),
    ("RIBALD",      "Coarsely vulgar"),
    ("SARDONIC",    "Grimly mocking"),
    ("TENUOUS",     "Very weak or slight"),
    ("URBANE",      "Suave and confident"),
    ("VERBOSE",     "Using more words than needed"),
    ("WHIMSICAL",   "Playfully quaint or fanciful"),
    # ── Extra Hard words ──
    ("ABJECT",      "Experienced to maximum degree"),
    ("ABROGATE",    "Repeal or do away with"),
    ("ABSOLVE",     "Set free from blame"),
    ("ABSTAIN",     "Refrain voluntarily"),
    ("ACCLAIM",     "Enthusiastic approval"),
    ("ACCOLADE",    "Award or expression of praise"),
    ("ACQUIESCE",   "Accept reluctantly but without protest"),
    ("ADAMANT",     "Refusing to be persuaded"),
    ("ADMONISH",    "Warn or reprimand gently"),
    ("ADROIT",      "Clever or skillful"),
    ("AFFABLE",     "Friendly and easy to talk to"),
    ("AGHAST",      "Struck with horror"),
    ("ALACRITY",    "Brisk eagerness"),
    ("ALIENATE",    "Make hostile or estranged"),
    ("ALLEGORY",    "Story with hidden meaning"),
    ("ALLEVIATE",   "Make suffering less severe"),
    ("ALTRUISM",    "Unselfish concern for others"),
    ("AMBIGUOUS",   "Open to multiple interpretations"),
    ("AMBIVALENT",  "Having mixed feelings"),
    ("AMELIORATE",  "Make bad situation better"),
    ("AMORPHOUS",   "Without definite shape"),
    ("ANACHRONISM", "Thing out of its time"),
    ("ANECDOTE",    "Short amusing story"),
    ("ANIMOSITY",   "Strong hostility"),
    ("ANOMALOUS",   "Deviating from the norm"),
    ("ANTIPATHY",   "Deep-seated dislike"),
    ("APATHETIC",   "Showing no interest"),
    ("APLOMB",      "Self-confidence and composure"),
    ("APPEASE",     "Pacify by conceding demands"),
    ("APPOSITE",    "Apt in context"),
    ("APPROBATION", "Approval or praise"),
    ("ARBITRARY",   "Based on random choice"),
    ("ARCANE",      "Mysterious and known by few"),
    ("ARDUOUS",     "Involving great effort"),
    ("ASCETIC",     "Practicing severe self-discipline"),
    ("ASPERSION",   "Attack on reputation"),
    ("ASSIDUOUS",   "Showing great care and effort"),
    ("ASTUTE",      "Clever at understanding"),
    ("ATROCIOUS",   "Horrifyingly wicked"),
    ("AUDACIOUS",   "Showing willingness to take bold risks"),
    ("AVARICE",     "Extreme greed for wealth"),
    ("AVERSION",    "Strong dislike or disinclination"),
    ("BANAL",       "Lacking originality"),
    ("BATHOS",      "Anticlimax in writing"),
    ("BEMOAN",      "Express discontent about"),
    ("BENIGN",      "Gentle and kind"),
    ("BERATE",      "Scold angrily"),
    ("BESIEGE",     "Surround with armed forces"),
    ("BLATANT",     "Done openly and unashamedly"),
    ("BLIGHT",      "Plant disease or spoil"),
    ("BOMBASTIC",   "High-sounding but empty"),
    ("BUCOLIC",     "Relating to pleasant countryside"),
    ("BUREAUCRACY",  "System of government with rigid rules"),
    ("BUOYANT",     "Able to float or cheerful"),
    ("CALLOUS",     "Showing no concern for others"),
    ("CANDOR",      "The quality of being open"),
    ("CANTANKEROUS","Bad-tempered and uncooperative"),
    ("CAPRICIOUS",  "Given to sudden change of mood"),
    ("CAUSTIC",     "Sarcastic in a scathing way"),
    ("CAVALIER",    "Showing disregard for others"),
    ("CENSURE",     "Express severe disapproval"),
    ("CHAGRIN",     "Distress at failure"),
    ("CHICANERY",   "Use of trickery to achieve goals"),
    ("CHRONIC",     "Persisting for a long time"),
    ("CIRCUITOUS",  "Longer than the most direct route"),
    ("CLANDESTINE", "Kept secret or done secretly"),
    ("COALESCE",    "Come together to form one mass"),
    ("COERCE",      "Persuade using threats"),
    ("COMPLACENT",  "Showing uncritical satisfaction"),
    ("CONCEDE",     "Admit something is true"),
    ("CONDONE",     "Accept behavior that is wrong"),
    ("CONJECTURE",  "Opinion without sufficient evidence"),
    ("CONVOLUTED",  "Extremely complex and difficult"),
    ("CORROBORATE", "Confirm or support a statement"),
    ("CRAVEN",      "Contemptibly lacking in courage"),
    ("CULPABLE",    "Deserving blame"),
    ("CURSORY",     "Hasty and not thorough"),
    ("CYNICISM",    "Distrust of human sincerity"),
    ("DAUNTLESS",   "Showing fearlessness"),
    ("DEBACLE",     "Sudden disastrous collapse"),
    ("DECADENT",    "Characterized by moral decay"),
    ("DECOROUS",    "In keeping with good taste"),
    ("DEFIANT",     "Showing bold resistance"),
    ("DEMAGOGUE",   "Political leader who uses emotion"),
    ("DEMURE",      "Reserved and modest"),
    ("DENOUNCE",    "Publicly declare to be wrong"),
    ("DEPRAVITY",   "Moral corruption"),
    ("DERISIVE",    "Expressing contempt or ridicule"),
    ("DESOLATE",    "Bleak and empty"),
    ("DESPONDENT",  "In low spirits from loss"),
    ("DESTITUTE",   "Without basic necessities"),
    ("DEVIOUS",     "Showing cunning or indirect way"),
    ("DEVOUT",      "Having strong religious belief"),
    ("DEXTEROUS",   "Skillful with hands"),
    ("DIFFIDENT",   "Modest or shy"),
    ("DILIGENT",    "Having steady careful effort"),
    ("DISCERN",     "Perceive or recognize"),
    ("DISDAIN",     "Feeling that something is unworthy"),
    ("DISMAL",      "Depressingly bad"),
    ("DISPARAGE",   "Regard as beneath consideration"),
    ("DISPEL",      "Make disappear"),
    ("DISSEMBLE",   "Conceal true motives"),
    ("DISSONANCE",  "Lack of harmony"),
    ("DISTRAUGHT",  "Deeply upset and agitated"),
    ("DOCILE",      "Obedient and easily managed"),
    ("DOGMATIC",    "Inclined to lay down principles"),
    ("DOLEFUL",     "Expressing grief or sorrow"),
    ("DUBIOUS",     "Hesitating or doubting"),
    ("DUPLICITY",   "Deceitfulness"),
    ("EARNEST",     "Showing sincere conviction"),
    ("ECCENTRIC",   "Unconventional and slightly strange"),
    ("EFFUSIVE",    "Expressing gratitude excessively"),
    ("ELOQUENT",    "Fluent or persuasive in speaking"),
    ("ELUSIVE",     "Difficult to find or achieve"),
    ("EMBELLISH",   "Make more attractive with detail"),
    ("EMINENT",     "Respected and successful"),
    ("EMPIRICAL",   "Based on observation or experience"),
    ("ENERVATE",    "Cause to feel drained of energy"),
    ("ENIGMA",      "Mysterious puzzling person"),
    ("ENTREAT",     "Ask someone earnestly"),
    ("EQUANIMITY",  "Mental calmness in difficulty"),
    ("ERRATIC",     "Not consistent or regular"),
    ("EVASIVE",     "Tending to avoid commitment"),
    ("EXEMPLARY",   "Serving as a desirable model"),
    ("EXORBITANT",  "Unreasonably high in price"),
    ("EXPEDIENT",   "Convenient and practical"),
    ("EXPLICIT",    "Stated clearly and in detail"),
    ("EXQUISITE",   "Extremely beautiful or delicate"),
    ("EXTOL",       "Praise enthusiastically"),
    ("EXUBERANT",   "Filled with lively energy"),
    ("FACILE",      "Appearing neat and simple"),
    ("FALLACIOUS",  "Based on mistaken belief"),
    ("FECKLESS",    "Lacking purpose or vitality"),
    ("FERVENT",     "Having passionate intensity"),
    ("FLAGRANT",    "Conspicuously wrong"),
    ("FLIPPANT",    "Not showing serious respect"),
    ("FLOURISH",    "Grow or develop well"),
    ("FOREBODING",  "Fearful feeling of future"),
    ("FORTHRIGHT",  "Direct and outspoken"),
    ("FRACAS",      "Noisy disturbance or fight"),
    ("FRUGAL",      "Sparing or economical"),
    ("FULSOME",     "Excessively complimentary"),
    ("FUTILE",      "Incapable of producing result"),
    ("GLIB",        "Fluent but insincere"),
    ("GRANDEUR",    "Splendor and impressiveness"),
    ("GRATUITOUS",  "Uncalled for or unwarranted"),
    ("GREGARIOUS",  "Fond of company"),
    ("GRIM",        "Serious and forbidding"),
    ("GUILELESS",   "Devoid of guile or deception"),
    ("GULLIBLE",    "Easily persuaded to believe"),
    ("HACKNEYED",   "Lacking originality from overuse"),
    ("HARANGUE",    "Lecture at length"),
    ("HAUGHTY",     "Arrogant and disdainful"),
    ("HEADSTRONG",  "Determined to do as one wishes"),
    ("HERETICAL",   "Contrary to accepted doctrine"),
    ("HOLLOW",      "Having empty space inside"),
    ("HOMOGENEOUS", "Of the same kind throughout"),
    ("HYPOCRITE",   "Person claiming virtues they lack"),
    ("ICONOCLAST",  "Person who attacks cherished beliefs"),
    ("IDIOSYNCRATIC","Peculiar to an individual"),
    ("IGNOMINIOUS", "Deserving or causing shame"),
    ("IMPERIOUS",   "Assuming power without justification"),
    ("IMPLACABLE",  "Unable to be appeased"),
    ("IMPLICIT",    "Implied though not stated"),
    ("IMPUDENT",    "Not showing due respect"),
    ("INARTICULATE","Unable to express clearly"),
    ("INCISIVE",    "Intelligently analytical"),
    ("INDOLENT",    "Wanting to avoid activity"),
    ("INDULGENT",   "Readily allowing gratification"),
    ("INEFFABLE",   "Too great to be expressed"),
    ("INSOLENT",    "Boldly rude or disrespectful"),
    ("INSIPID",     "Lacking vigor or interest"),
    ("INTREPID",    "Fearless and adventurous"),
    ("INVECTIVE",   "Insulting or abusive language"),
    ("IRASCIBLE",   "Having a tendency to be angry"),
    ("IRREVERENT",  "Showing disrespect"),
    ("LABYRINTH",   "Complicated irregular network"),
    ("LATENT",      "Existing but not yet developed"),
    ("LAUD",        "Praise highly"),
    ("LETHARGIC",   "Sluggish and apathetic"),
    ("LICENTIOUS",  "Promiscuous and unprincipled"),
    ("LUGUBRIOUS",  "Looking or sounding sad"),
    ("MAGNANIMOUS", "Generous in forgiving"),
    ("MALEVOLENT",  "Having wish to do evil"),
    ("MALLEABLE",   "Easily influenced or shaped"),
    ("MANIFOLD",    "Many and varied"),
    ("MARTYR",      "Person who suffers for beliefs"),
    ("MERCURIAL",   "Subject to sudden changes"),
    ("METICULOUS",  "Showing great attention to detail"),
    ("MIRTH",       "Great amusement and laughter"),
    ("MITIGATE",    "Make less severe"),
    ("MORDANT",     "Having a sharp cutting quality"),
    ("MOROSE",      "Sullen and ill-tempered"),
    ("MUNDANE",     "Lacking interest or excitement"),
    ("MUNIFICENT",  "More generous than expected"),
    ("NARCISSISTIC","Excessive admiration of oneself"),
    ("NONCHALANT",  "Feeling no concern"),
    ("OBSTINATE",   "Stubbornly refusing to change"),
    ("OMINOUS",     "Giving impression of evil"),
    ("OPULENT",     "Ostentatiously rich"),
    ("ORNATE",      "Elaborately decorated"),
    ("OSTENTATIOUS","Designed to impress"),
    ("OUTLANDISH",  "Bizarre or unfamiliar"),
    ("PALPABLE",    "Able to be touched or felt"),
    ("PARADOX",     "Seemingly absurd but true statement"),
    ("PATRONIZE",   "Treat as if inferior"),
    ("PENSIVE",     "Engaged in deep thought"),
    ("PEREMPTORY",  "Insisting on immediate obedience"),
    ("PERFIDIOUS",  "Deceitful and untrustworthy"),
    ("PERSPICACIOUS","Having ready insight into things"),
    ("PETULANT",    "Childishly sulky"),
    ("PHLEGMATIC",  "Having unemotional calm nature"),
    ("PLATITUDE",   "Remark stated as if profound"),
    ("PLAUSIBLE",   "Seeming reasonable or probable"),
    ("POMPOUS",     "Affectedly grand"),
    ("PRECARIOUS",  "Not securely held"),
    ("PRECIPITOUS", "Dangerously high or steep"),
    ("PRESUMPTUOUS","Failing to observe proper limits"),
    ("PREVARICATE", "Speak or act evasively"),
    ("PRODIGAL",    "Spending money recklessly"),
    ("PRODIGIOUS",  "Remarkably great"),
    ("PROFLIGATE",  "Recklessly extravagant"),
    ("PROLIFIC",    "Producing much output"),
    ("PROPITIOUS",  "Giving indication of good result"),
    ("PRUDENT",     "Acting with care and forethought"),
    ("PUGNACIOUS",  "Eager to argue or fight"),
    ("PUSILLANIMOUS","Showing lack of courage"),
    ("QUANDARY",    "State of uncertainty"),
    ("RAPACIOUS",   "Aggressively greedy"),
    ("RAUCOUS",     "Making harsh noisy sounds"),
    ("RECLUSIVE",   "Avoiding contact with others"),
    ("RETICENT",    "Not revealing thoughts readily"),
    ("REVERENCE",   "Deep respect for something"),
    ("RHETORIC",    "Persuasive language"),
    ("RIGHTEOUS",   "Morally justified"),
    ("RUTHLESS",    "Having no compassion"),
    ("SANCTIMONIOUS","Making show of being holy"),
    ("SCRUPULOUS",  "Diligent and careful"),
    ("SENTIMENTAL", "Excessively tender or nostalgic"),
    ("SERENDIPITY", "Fortunate accident or discovery"),
    ("SHREWD",      "Having good practical judgment"),
    ("SKEPTICAL",   "Not easily convinced"),
    ("SLOVENLY",    "Messy and careless"),
    ("SOLEMN",      "Formal and dignified"),
    ("SOMBER",      "Dark or dull in color"),
    ("SOPHISTRY",   "Use of clever but false argument"),
    ("SQUALID",     "Extremely dirty and unpleasant"),
    ("STOIC",       "Enduring pain without complaint"),
    ("STRIDENT",    "Loud and harsh"),
    ("SUBDUED",     "Quiet and restrained"),
    ("SUBTLETY",    "Fineness or delicacy of meaning"),
    ("SULLEN",      "Moody and resentful"),
    ("SUPERCILIOUS","Behaving as superior"),
    ("SURREPTITIOUS","Done secretly"),
    ("SYCOPHANCY",  "Excessive flattery"),
    ("TACIT",       "Understood without being stated"),
    ("TEDIOUS",     "Too long and slow"),
    ("TEMERITY",    "Excessive boldness"),
    ("TEMPERATE",   "Showing moderation and restraint"),
    ("TIMOROUS",    "Showing fear or hesitancy"),
    ("TORPOR",      "State of physical inactivity"),
    ("TRANSGRESS",  "Go beyond limits of what is allowed"),
    ("TRITE",       "Overused and lacking freshness"),
    ("TURBULENT",   "Moving unsteadily"),
    ("TYRANNY",     "Cruel use of power"),
    ("UNCANNY",     "Strange or mysterious"),
    ("UNDERMINE",   "Weaken or damage gradually"),
    ("UNDULATE",    "Move with wavelike motion"),
    ("UNSAVORY",    "Disagreeable or objectionable"),
    ("UNTENABLE",   "Not able to be maintained"),
    ("USURPATION",  "Taking power by force"),
    ("VACILLATE",   "Waver between opinions"),
    ("VANQUISH",    "Defeat thoroughly"),
    ("VENERABLE",   "Accorded great respect"),
    ("VERACIOUS",   "Speaking or representing truth"),
    ("VEXATIOUS",   "Causing annoyance"),
    ("VIGILANT",    "Keeping careful watch"),
    ("VINDICTIVE",  "Having strong revenge desire"),
    ("VIRULENT",    "Extremely severe or harmful"),
    ("VITRIOLIC",   "Filled with bitter criticism"),
    ("VOLATILE",    "Liable to change rapidly"),
    ("VULNERABLE",  "Susceptible to attack or harm"),
    ("WARY",        "Feeling cautious about"),
    ("XENOPHOBIA",  "Dislike of people from other countries"),
    ("ZEALOTRY",    "Fanatical devotion"),
],
}


# ─────────────────────────────────────────────────────────────
# 3. DATA CLASSES
# ─────────────────────────────────────────────────────────────
@dataclass
class PlacedWord:
    word: str
    clue: str
    row: int
    col: int
    direction: str   # "A" = across, "D" = down
    number: int = 0


class AppState:
    def __init__(self):
        self.difficulty: str = "Easy"
        self.placed_words: List[PlacedWord] = []
        self.solution: List[List[Optional[str]]] = []
        self.cells: List[List[dict]] = []
        self.grid_size: int = 9
        self.selected_row: int = -1
        self.selected_col: int = -1
        self.direction: str = "A"
        self.active_word: Optional[PlacedWord] = None
        self.check_mode: bool = False
        self.start_time: float = 0.0
        self.elapsed_stopped: Optional[float] = None

    def reset_cells(self):
        size = self.grid_size
        self.cells = [
            [
                {
                    "letter": "",
                    "checked": False,
                    "correct": False,
                    "revealed": False,
                }
                for _ in range(size)
            ]
            for _ in range(size)
        ]


# ─────────────────────────────────────────────────────────────
# 4. CROSSWORD GENERATOR
# ─────────────────────────────────────────────────────────────
class CrosswordGenerator:
    def __init__(self, difficulty: str):
        cfg = DIFFICULTY_SETTINGS[difficulty]
        self.size: int = cfg["size"]
        self.min_len: int = cfg["min_len"]
        self.max_len: int = cfg["max_len"]
        self.target: int = cfg["word_count"]
        self.grid: List[List[Optional[str]]] = [[None] * self.size for _ in range(self.size)]
        self.placed: List[PlacedWord] = []
        all_words = WORD_BANKS[difficulty][:]
        random.shuffle(all_words)
        filtered = [(w, c) for w, c in all_words if self.min_len <= len(w) <= self.max_len]
        # oversample by 3x
        self.candidates = filtered * 3
        random.shuffle(self.candidates)

    def generate(self) -> Tuple[List[PlacedWord], List[List[Optional[str]]]]:
        target = self.target
        for _ in range(5):
            self._reset()
            self._attempt(target)
            if len(self.placed) >= target * 0.6:
                break
            target = max(6, target - 2)

        self._assign_numbers()
        return self.placed, [row[:] for row in self.grid]

    def _reset(self):
        self.grid = [[None] * self.size for _ in range(self.size)]
        self.placed = []

    def _attempt(self, target: int):
        pool = self.candidates[:]
        random.shuffle(pool)
        used_words = set()

        # Place first word horizontally, centered
        for word, clue in pool:
            if len(word) <= self.size:
                r = self.size // 2
                c = (self.size - len(word)) // 2
                self._place_word(word, clue, r, c, "A")
                used_words.add(word)
                break

        if not self.placed:
            return

        remaining = [(w, c) for w, c in pool if w not in used_words]
        random.shuffle(remaining)

        for word, clue in remaining:
            if len(self.placed) >= target:
                break
            if word in used_words:
                continue
            best = self._find_best_placement(word)
            if best is not None:
                r, c, d = best
                self._place_word(word, clue, r, c, d)
                used_words.add(word)

    def _find_best_placement(self, word: str) -> Optional[Tuple[int, int, str]]:
        candidates = []
        for direction in ("A", "D"):
            for r in range(self.size):
                for c in range(self.size):
                    if self._can_place(word, r, c, direction):
                        score = self._score_placement(word, r, c, direction)
                        candidates.append((score, r, c, direction))
        if not candidates:
            return None
        candidates.sort(key=lambda x: -x[0])
        # pick from top candidates randomly for variety
        top = candidates[:max(1, len(candidates) // 4)]
        chosen = random.choice(top)
        return chosen[1], chosen[2], chosen[3]

    def _can_place(self, word: str, row: int, col: int, direction: str) -> bool:
        dr, dc = (0, 1) if direction == "A" else (1, 0)
        length = len(word)

        # 1. All cells in bounds
        end_r = row + dr * (length - 1)
        end_c = col + dc * (length - 1)
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        if not (0 <= end_r < self.size and 0 <= end_c < self.size):
            return False

        # 2. Head cell before start must be None or OOB
        hr, hc = row - dr, col - dc
        if 0 <= hr < self.size and 0 <= hc < self.size:
            if self.grid[hr][hc] is not None:
                return False

        # 3. Tail cell after end must be None or OOB
        tr, tc = end_r + dr, end_c + dc
        if 0 <= tr < self.size and 0 <= tc < self.size:
            if self.grid[tr][tc] is not None:
                return False

        # 4 & 5. Per-cell validation
        has_intersection = False
        for i, letter in enumerate(word):
            r = row + dr * i
            c = col + dc * i
            existing = self.grid[r][c]

            if existing is not None:
                # Must be a matching letter
                if existing != letter:
                    return False
                has_intersection = True
            else:
                # Empty cell: check perpendicular neighbors for adjacency
                perp_r, perp_c = (1, 0) if direction == "A" else (0, 1)
                for side in (-1, 1):
                    nr = r + perp_r * side
                    nc = c + perp_c * side
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        if self.grid[nr][nc] is not None:
                            return False

        # 6. Must have >= 1 intersection (except first word)
        if self.placed and not has_intersection:
            return False

        return True

    def _score_placement(self, word: str, row: int, col: int, direction: str) -> int:
        dr, dc = (0, 1) if direction == "A" else (1, 0)
        intersections = 0
        edge_penalty = 0

        for i in range(len(word)):
            r = row + dr * i
            c = col + dc * i
            if self.grid[r][c] is not None:
                intersections += 1
            # penalize cells near edges
            edge_dist = min(r, self.size - 1 - r, c, self.size - 1 - c)
            if edge_dist == 0:
                edge_penalty += 3
            elif edge_dist == 1:
                edge_penalty += 1

        return intersections * 10 - edge_penalty + random.randint(0, 3)

    def _place_word(self, word: str, clue: str, row: int, col: int, direction: str):
        dr, dc = (0, 1) if direction == "A" else (1, 0)
        for i, letter in enumerate(word):
            self.grid[row + dr * i][col + dc * i] = letter
        pw = PlacedWord(word=word, clue=clue, row=row, col=col, direction=direction)
        self.placed.append(pw)

    def _assign_numbers(self):
        # Scan grid in reading order; assign number if any word starts here
        num = 1
        starts: Dict[Tuple[int, int], int] = {}

        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] is None:
                    continue
                needs_number = False
                for pw in self.placed:
                    if pw.row == r and pw.col == c:
                        needs_number = True
                        break
                if needs_number:
                    if (r, c) not in starts:
                        starts[(r, c)] = num
                        num += 1

        for pw in self.placed:
            pw.number = starts.get((pw.row, pw.col), 0)

        # Sort placed words by number then direction for clean display
        self.placed.sort(key=lambda p: (p.number, p.direction))


# ─────────────────────────────────────────────────────────────
# 5. GUI CLASSES
# ─────────────────────────────────────────────────────────────

class CluePanel(tk.Frame):
    def __init__(self, parent, on_clue_click, **kwargs):
        super().__init__(parent, bg=COLORS["clue_bg"], **kwargs)
        self._on_clue_click = on_clue_click
        self._across_words: List[PlacedWord] = []
        self._down_words: List[PlacedWord] = []
        self._build()

    def _build(self):
        # Across section
        across_label = tk.Label(
            self, text="ACROSS", font=("Helvetica", 10, "bold"),
            bg=COLORS["clue_bg"], anchor="w", padx=6, pady=4
        )
        across_label.pack(fill=tk.X)

        across_frame = tk.Frame(self, bg=COLORS["clue_bg"])
        across_frame.pack(fill=tk.BOTH, expand=True)

        self.across_scroll = tk.Scrollbar(across_frame, orient=tk.VERTICAL)
        self.across_list = tk.Listbox(
            across_frame, yscrollcommand=self.across_scroll.set,
            font=("Helvetica", 9), selectmode=tk.SINGLE,
            bg=COLORS["clue_bg"], relief=tk.FLAT,
            selectbackground=COLORS["clue_active"], selectforeground="white",
            activestyle="none", height=12
        )
        self.across_scroll.config(command=self.across_list.yview)
        self.across_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.across_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.across_list.bind("<<ListboxSelect>>", self._on_across_select)

        # Separator
        tk.Frame(self, height=2, bg="#cccccc").pack(fill=tk.X)

        # Down section
        down_label = tk.Label(
            self, text="DOWN", font=("Helvetica", 10, "bold"),
            bg=COLORS["clue_bg"], anchor="w", padx=6, pady=4
        )
        down_label.pack(fill=tk.X)

        down_frame = tk.Frame(self, bg=COLORS["clue_bg"])
        down_frame.pack(fill=tk.BOTH, expand=True)

        self.down_scroll = tk.Scrollbar(down_frame, orient=tk.VERTICAL)
        self.down_list = tk.Listbox(
            down_frame, yscrollcommand=self.down_scroll.set,
            font=("Helvetica", 9), selectmode=tk.SINGLE,
            bg=COLORS["clue_bg"], relief=tk.FLAT,
            selectbackground=COLORS["clue_active"], selectforeground="white",
            activestyle="none", height=12
        )
        self.down_scroll.config(command=self.down_list.yview)
        self.down_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.down_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.down_list.bind("<<ListboxSelect>>", self._on_down_select)

    def populate(self, across_words: List[PlacedWord], down_words: List[PlacedWord]):
        self._across_words = across_words
        self._down_words = down_words
        self.across_list.delete(0, tk.END)
        self.down_list.delete(0, tk.END)
        for pw in across_words:
            self.across_list.insert(tk.END, f"  {pw.number}. {pw.clue}")
        for pw in down_words:
            self.down_list.insert(tk.END, f"  {pw.number}. {pw.clue}")

    def highlight_clue(self, active_word: Optional[PlacedWord]):
        self.across_list.selection_clear(0, tk.END)
        self.down_list.selection_clear(0, tk.END)
        if active_word is None:
            return
        if active_word.direction == "A":
            for i, pw in enumerate(self._across_words):
                if pw is active_word:
                    self.across_list.selection_set(i)
                    self.across_list.see(i)
                    return
        else:
            for i, pw in enumerate(self._down_words):
                if pw is active_word:
                    self.down_list.selection_set(i)
                    self.down_list.see(i)
                    return

    def _on_across_select(self, event):
        sel = self.across_list.curselection()
        if sel and self._across_words:
            idx = sel[0]
            if idx < len(self._across_words):
                self.down_list.selection_clear(0, tk.END)
                self._on_clue_click(self._across_words[idx])

    def _on_down_select(self, event):
        sel = self.down_list.curselection()
        if sel and self._down_words:
            idx = sel[0]
            if idx < len(self._down_words):
                self.across_list.selection_clear(0, tk.END)
                self._on_clue_click(self._down_words[idx])


class GridCanvas(tk.Canvas):
    def __init__(self, parent, state: AppState, on_cell_click, **kwargs):
        kwargs.setdefault("bg", COLORS["black_cell"])
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.state = state
        self._on_cell_click = on_cell_click
        self.cell_size = CELL_MIN
        self._letter_font = None
        self._number_font = None
        self.bind("<Button-1>", self._on_click)
        self.bind("<Configure>", self._on_configure)

    def _update_fonts(self):
        cs = self.cell_size
        letter_size = max(8, int(cs * 0.55))
        number_size = max(5, int(cs * 0.22))
        self._letter_font = tkfont.Font(family="Helvetica", size=letter_size, weight="bold")
        self._number_font = tkfont.Font(family="Helvetica", size=number_size)

    def draw_grid(self):
        self.delete("all")
        st = self.state
        if not st.solution:
            return

        size = st.grid_size
        cs = self.cell_size
        self._update_fonts()

        # Determine which cells belong to active word
        active_cells = set()
        if st.active_word:
            aw = st.active_word
            dr, dc = (0, 1) if aw.direction == "A" else (1, 0)
            for i in range(len(aw.word)):
                active_cells.add((aw.row + dr * i, aw.col + dc * i))

        for r in range(size):
            for c in range(size):
                x1 = MARGIN + c * cs
                y1 = MARGIN + r * cs
                x2 = x1 + cs
                y2 = y1 + cs

                sol_letter = st.solution[r][c]

                if sol_letter is None:
                    # Black cell
                    self.create_rectangle(x1, y1, x2, y2, fill=COLORS["black_cell"], outline="")
                    continue

                cell = st.cells[r][c]

                # Determine fill color by priority
                if (r, c) == (st.selected_row, st.selected_col):
                    fill = COLORS["selected_cell"]
                elif (r, c) in active_cells:
                    if cell["revealed"]:
                        fill = COLORS["revealed_cell"]
                    elif cell["checked"] and cell["correct"]:
                        fill = COLORS["correct_cell"]
                    else:
                        fill = COLORS["word_highlight"]
                elif cell["revealed"]:
                    fill = COLORS["revealed_cell"]
                elif cell["checked"] and cell["correct"]:
                    fill = COLORS["correct_cell"]
                else:
                    fill = COLORS["white_cell"]

                self.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#cccccc", width=1)

                # Clue number
                num = self._get_cell_number(r, c)
                if num:
                    self.create_text(
                        x1 + 2, y1 + 2,
                        text=str(num),
                        anchor="nw",
                        font=self._number_font,
                        fill=COLORS["number_text"]
                    )

                # Letter
                letter = cell["letter"]
                if letter:
                    # Determine text color
                    if cell["revealed"]:
                        txt_color = "#5500aa"
                    elif cell["checked"] and not cell["correct"]:
                        txt_color = COLORS["error_text"]
                    else:
                        txt_color = COLORS["normal_text"]

                    self.create_text(
                        (x1 + x2) // 2, (y1 + y2) // 2,
                        text=letter,
                        font=self._letter_font,
                        fill=txt_color
                    )

    def _get_cell_number(self, r: int, c: int) -> int:
        for pw in self.state.placed_words:
            if pw.row == r and pw.col == c:
                return pw.number
        return 0

    def _on_click(self, event):
        r, c = self._pixel_to_cell(event.x, event.y)
        if r < 0 or c < 0 or r >= self.state.grid_size or c >= self.state.grid_size:
            return
        if self.state.solution[r][c] is None:
            return
        self._on_cell_click(r, c)

    def _on_configure(self, event):
        if not self.state.solution:
            return
        w = event.width - MARGIN * 2
        h = event.height - MARGIN * 2
        size = self.state.grid_size
        cs = max(CELL_MIN, min(w // size, h // size))
        self.cell_size = cs
        self.draw_grid()

    def _pixel_to_cell(self, x: int, y: int) -> Tuple[int, int]:
        cs = self.cell_size
        r = (y - MARGIN) // cs
        c = (x - MARGIN) // cs
        return r, c


class CrosswordApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crossword Puzzle")
        self.geometry("900x650")
        self.minsize(700, 500)
        self.configure(bg=COLORS["black_cell"])

        self.state = AppState()
        self._game_frame: Optional[tk.Frame] = None
        self._timer_label: Optional[tk.Label] = None
        self._canvas: Optional[GridCanvas] = None
        self._clue_panel: Optional[CluePanel] = None
        self._tick_id = None

        self.show_start_screen()

    # ── Start Screen ──────────────────────────────────────────
    def show_start_screen(self):
        if self._game_frame:
            self._game_frame.destroy()
            self._game_frame = None
        self._stop_timer()

        frame = tk.Frame(self, bg=COLORS["black_cell"])
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            frame, text="CROSSWORD", font=("Helvetica", 36, "bold"),
            fg="white", bg=COLORS["black_cell"]
        ).pack(pady=(0, 8))

        tk.Label(
            frame, text="Choose a difficulty to begin",
            font=("Helvetica", 13), fg="#aaaaaa", bg=COLORS["black_cell"]
        ).pack(pady=(0, 30))

        btn_style = dict(
            font=("Helvetica", 14, "bold"), width=16, relief=tk.FLAT,
            cursor="hand2", pady=10
        )

        colors = [("#4caf50", "Easy"), ("#2196f3", "Medium"), ("#f44336", "Hard")]
        for color, diff in colors:
            b = tk.Button(
                frame, text=diff, bg=color, fg="white",
                command=lambda d=diff: self.start_game(d),
                activebackground=color, activeforeground="white",
                **btn_style
            )
            b.pack(pady=6)

        self._start_frame = frame

    # ── Game Start ────────────────────────────────────────────
    def start_game(self, difficulty: str):
        if hasattr(self, "_start_frame") and self._start_frame:
            self._start_frame.destroy()

        self.state.difficulty = difficulty
        self._run_generator()
        self._build_game_screen()
        self._bind_keys()
        self._start_timer()

    def _run_generator(self):
        st = self.state
        cfg = DIFFICULTY_SETTINGS[st.difficulty]
        st.grid_size = cfg["size"]
        gen = CrosswordGenerator(st.difficulty)
        placed, solution = gen.generate()
        st.placed_words = placed
        st.solution = solution
        st.reset_cells()
        st.check_mode = False
        st.elapsed_stopped = None
        # Select first word
        if placed:
            first = placed[0]
            st.selected_row = first.row
            st.selected_col = first.col
            st.direction = first.direction
            st.active_word = first
        else:
            st.selected_row = 0
            st.selected_col = 0
            st.direction = "A"
            st.active_word = None

    def _build_game_screen(self):
        if self._game_frame:
            self._game_frame.destroy()

        self._game_frame = tk.Frame(self, bg=COLORS["black_cell"])
        self._game_frame.pack(fill=tk.BOTH, expand=True)

        self._build_toolbar(self._game_frame)

        content = tk.Frame(self._game_frame, bg=COLORS["black_cell"])
        content.pack(fill=tk.BOTH, expand=True)

        # Grid canvas
        self._canvas = GridCanvas(
            content, self.state, self._on_cell_click,
            bg=COLORS["black_cell"]
        )
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(4, 2), pady=4)

        # Clue panel
        self._clue_panel = CluePanel(content, self._on_clue_click, width=260)
        self._clue_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(2, 4), pady=4)
        self._clue_panel.pack_propagate(False)

        self._populate_clues()
        self.update_idletasks()
        # Compute initial cell size
        w = self._canvas.winfo_width()
        h = self._canvas.winfo_height()
        if w > 1 and h > 1:
            size = self.state.grid_size
            cs = max(CELL_MIN, min((w - MARGIN * 2) // size, (h - MARGIN * 2) // size))
            self._canvas.cell_size = cs
        self._canvas.draw_grid()
        self._sync_clue_panel()

    def _build_toolbar(self, parent):
        toolbar = tk.Frame(parent, bg=COLORS["toolbar_bg"], height=44)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        toolbar.pack_propagate(False)

        btn_style = dict(
            bg="#444444", fg=COLORS["toolbar_fg"],
            font=("Helvetica", 10, "bold"), relief=tk.FLAT,
            padx=12, pady=6, cursor="hand2",
            activebackground="#666666", activeforeground="white"
        )

        tk.Button(toolbar, text="New Puzzle", command=self.new_puzzle, **btn_style).pack(
            side=tk.LEFT, padx=(8, 4), pady=6
        )
        tk.Button(toolbar, text="Check", command=self.check_answers, **btn_style).pack(
            side=tk.LEFT, padx=4, pady=6
        )
        tk.Button(toolbar, text="Reveal", command=self.reveal_answers, **btn_style).pack(
            side=tk.LEFT, padx=4, pady=6
        )

        # Difficulty label
        diff_label = tk.Label(
            toolbar, text=self.state.difficulty,
            font=("Helvetica", 10), fg="#aaaaaa", bg=COLORS["toolbar_bg"]
        )
        diff_label.pack(side=tk.LEFT, padx=16)

        # Timer
        self._timer_label = tk.Label(
            toolbar, text="0:00",
            font=("Helvetica", 13, "bold"), fg="white", bg=COLORS["toolbar_bg"],
            width=6
        )
        self._timer_label.pack(side=tk.RIGHT, padx=16)

        # Change difficulty buttons
        for diff, color in [("Easy", "#4caf50"), ("Medium", "#2196f3"), ("Hard", "#f44336")]:
            b = tk.Button(
                toolbar, text=diff, bg=color, fg="white",
                font=("Helvetica", 9, "bold"), relief=tk.FLAT,
                padx=8, pady=5, cursor="hand2",
                activebackground=color, activeforeground="white",
                command=lambda d=diff: self._change_difficulty(d)
            )
            b.pack(side=tk.RIGHT, padx=3, pady=6)

    def _change_difficulty(self, difficulty: str):
        self.state.difficulty = difficulty
        self._stop_timer()
        self._run_generator()
        if self._game_frame:
            self._game_frame.destroy()
            self._game_frame = None
        self._build_game_screen()
        self._start_timer()

    def _populate_clues(self):
        if not self._clue_panel:
            return
        across = [pw for pw in self.state.placed_words if pw.direction == "A"]
        down = [pw for pw in self.state.placed_words if pw.direction == "D"]
        across.sort(key=lambda p: p.number)
        down.sort(key=lambda p: p.number)
        self._clue_panel.populate(across, down)

    # ── Key Bindings ──────────────────────────────────────────
    def _bind_keys(self):
        self.bind("<Key>", self._on_key)
        self.focus_set()

    def _on_key(self, event):
        st = self.state
        if not st.solution:
            return

        keysym = event.keysym
        char = event.char.upper() if event.char else ""

        if keysym == "Tab":
            self._cycle_word(forward=True)
        elif keysym == "ISO_Left_Tab" or (keysym == "Tab" and (event.state & 0x1)):
            self._cycle_word(forward=False)
        elif keysym == "BackSpace":
            self._handle_backspace()
        elif keysym in ("Left", "Right", "Up", "Down"):
            self._handle_arrow(keysym)
        elif char and char.isalpha() and len(char) == 1:
            self._handle_letter(char)

    def _handle_letter(self, letter: str):
        st = self.state
        r, c = st.selected_row, st.selected_col
        if r < 0 or c < 0:
            return
        if st.solution[r][c] is None:
            return
        cell = st.cells[r][c]
        cell["letter"] = letter
        cell["checked"] = False
        cell["correct"] = False
        st.check_mode = False
        self._advance_cursor()
        self._canvas.draw_grid()
        self._check_completion()

    def _handle_backspace(self):
        st = self.state
        r, c = st.selected_row, st.selected_col
        if r < 0 or c < 0:
            return
        cell = st.cells[r][c]
        if cell["letter"] and not cell["revealed"]:
            cell["letter"] = ""
            cell["checked"] = False
            cell["correct"] = False
        else:
            self._retreat_cursor()
            r2, c2 = st.selected_row, st.selected_col
            if (r2, c2) != (r, c):
                cell2 = st.cells[r2][c2]
                if not cell2["revealed"]:
                    cell2["letter"] = ""
                    cell2["checked"] = False
                    cell2["correct"] = False
        self._canvas.draw_grid()

    def _handle_arrow(self, keysym: str):
        st = self.state
        arrow_map = {
            "Left":  (0, -1, "A"),
            "Right": (0,  1, "A"),
            "Up":    (-1, 0, "D"),
            "Down":  (1,  0, "D"),
        }
        dr, dc, arrow_dir = arrow_map[keysym]

        if st.direction == arrow_dir:
            # Move in current direction
            self._move_cursor(dr, dc)
        else:
            # Change direction
            st.direction = arrow_dir
            self._update_active_word()
            self._sync_clue_panel()
            self._canvas.draw_grid()

    def _advance_cursor(self):
        st = self.state
        dr, dc = (0, 1) if st.direction == "A" else (1, 0)
        r, c = st.selected_row + dr, st.selected_col + dc
        if 0 <= r < st.grid_size and 0 <= c < st.grid_size and st.solution[r][c] is not None:
            st.selected_row, st.selected_col = r, c
            self._update_active_word()
            self._sync_clue_panel()

    def _retreat_cursor(self):
        st = self.state
        dr, dc = (0, 1) if st.direction == "A" else (1, 0)
        r, c = st.selected_row - dr, st.selected_col - dc
        if 0 <= r < st.grid_size and 0 <= c < st.grid_size and st.solution[r][c] is not None:
            st.selected_row, st.selected_col = r, c
            self._update_active_word()
            self._sync_clue_panel()

    def _move_cursor(self, dr: int, dc: int):
        st = self.state
        r, c = st.selected_row + dr, st.selected_col + dc
        while 0 <= r < st.grid_size and 0 <= c < st.grid_size:
            if st.solution[r][c] is not None:
                st.selected_row, st.selected_col = r, c
                self._update_active_word()
                self._sync_clue_panel()
                self._canvas.draw_grid()
                return
            r += dr
            c += dc

    def _cycle_word(self, forward: bool):
        st = self.state
        if not st.placed_words:
            return
        words_in_order = sorted(st.placed_words, key=lambda p: (p.number, 0 if p.direction == "A" else 1))
        current_idx = None
        if st.active_word:
            for i, pw in enumerate(words_in_order):
                if pw is st.active_word:
                    current_idx = i
                    break
        if current_idx is None:
            current_idx = 0
        else:
            step = 1 if forward else -1
            current_idx = (current_idx + step) % len(words_in_order)
        pw = words_in_order[current_idx]
        st.selected_row = pw.row
        st.selected_col = pw.col
        st.direction = pw.direction
        st.active_word = pw
        self._sync_clue_panel()
        self._canvas.draw_grid()

    # ── Cell Click ────────────────────────────────────────────
    def _on_cell_click(self, r: int, c: int):
        st = self.state
        if (r, c) == (st.selected_row, st.selected_col):
            # Toggle direction
            new_dir = "D" if st.direction == "A" else "A"
            # Check if a word exists in new direction
            for pw in st.placed_words:
                dr2, dc2 = (0, 1) if pw.direction == "A" else (1, 0)
                cells_in_word = {(pw.row + dr2 * i, pw.col + dc2 * i) for i in range(len(pw.word))}
                if (r, c) in cells_in_word and pw.direction == new_dir:
                    st.direction = new_dir
                    break
        else:
            st.selected_row = r
            st.selected_col = c
            # Prefer current direction if word exists there
            found = self._find_word_at(r, c, st.direction)
            if not found:
                alt_dir = "D" if st.direction == "A" else "A"
                found = self._find_word_at(r, c, alt_dir)
                if found:
                    st.direction = alt_dir

        self._update_active_word()
        self._sync_clue_panel()
        self._canvas.draw_grid()
        self.focus_set()

    def _find_word_at(self, r: int, c: int, direction: str) -> Optional[PlacedWord]:
        for pw in self.state.placed_words:
            if pw.direction != direction:
                continue
            dr, dc = (0, 1) if direction == "A" else (1, 0)
            for i in range(len(pw.word)):
                if pw.row + dr * i == r and pw.col + dc * i == c:
                    return pw
        return None

    def _on_clue_click(self, pw: PlacedWord):
        st = self.state
        st.selected_row = pw.row
        st.selected_col = pw.col
        st.direction = pw.direction
        st.active_word = pw
        self._sync_clue_panel()
        self._canvas.draw_grid()
        self.focus_set()

    # ── State Updates ─────────────────────────────────────────
    def _update_active_word(self):
        st = self.state
        r, c = st.selected_row, st.selected_col
        found = self._find_word_at(r, c, st.direction)
        if found:
            st.active_word = found
        else:
            # Try other direction
            alt = "D" if st.direction == "A" else "A"
            found2 = self._find_word_at(r, c, alt)
            if found2:
                st.active_word = found2
                st.direction = alt
            else:
                st.active_word = None

    def _sync_clue_panel(self):
        if self._clue_panel:
            self._clue_panel.highlight_clue(self.state.active_word)

    # ── Game Actions ──────────────────────────────────────────
    def new_puzzle(self):
        self._stop_timer()
        self._run_generator()
        self._populate_clues()
        self._update_active_word()
        self._sync_clue_panel()
        self._canvas.draw_grid()
        self._start_timer()
        self.focus_set()

    def check_answers(self):
        st = self.state
        st.check_mode = True
        for r in range(st.grid_size):
            for c in range(st.grid_size):
                if st.solution[r][c] is None:
                    continue
                cell = st.cells[r][c]
                if cell["letter"] and not cell["revealed"]:
                    cell["checked"] = True
                    cell["correct"] = (cell["letter"] == st.solution[r][c])
        self._canvas.draw_grid()

    def reveal_answers(self):
        st = self.state
        for r in range(st.grid_size):
            for c in range(st.grid_size):
                if st.solution[r][c] is not None:
                    cell = st.cells[r][c]
                    cell["letter"] = st.solution[r][c]
                    cell["revealed"] = True
                    cell["checked"] = False
                    cell["correct"] = False
        self._stop_timer()
        self._canvas.draw_grid()

    def _check_completion(self):
        st = self.state
        for r in range(st.grid_size):
            for c in range(st.grid_size):
                if st.solution[r][c] is None:
                    continue
                cell = st.cells[r][c]
                if cell["letter"] != st.solution[r][c]:
                    return
        # All correct!
        self._stop_timer()
        elapsed = st.elapsed_stopped or (time.time() - st.start_time)
        mins = int(elapsed) // 60
        secs = int(elapsed) % 60
        dialog = tk.Toplevel(self)
        dialog.title("Congratulations!")
        dialog.geometry("320x180")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.configure(bg=COLORS["black_cell"])
        tk.Label(
            dialog, text="Puzzle Complete!", font=("Helvetica", 20, "bold"),
            fg="#4caf50", bg=COLORS["black_cell"]
        ).pack(pady=20)
        tk.Label(
            dialog, text=f"Time: {mins}:{secs:02d}",
            font=("Helvetica", 14), fg="white", bg=COLORS["black_cell"]
        ).pack()
        tk.Button(
            dialog, text="New Puzzle", font=("Helvetica", 12, "bold"),
            bg="#4caf50", fg="white", relief=tk.FLAT, padx=16, pady=8,
            cursor="hand2",
            command=lambda: (dialog.destroy(), self.new_puzzle())
        ).pack(pady=20)

    # ── Timer ──────────────────────────────────────────────────
    def _start_timer(self):
        self.state.start_time = time.time()
        self.state.elapsed_stopped = None
        self._tick()

    def _stop_timer(self):
        if self._tick_id:
            self.after_cancel(self._tick_id)
            self._tick_id = None
        if self.state.start_time and self.state.elapsed_stopped is None:
            self.state.elapsed_stopped = time.time() - self.state.start_time

    def _tick(self):
        if self.state.elapsed_stopped is not None:
            return
        elapsed = time.time() - self.state.start_time
        mins = int(elapsed) // 60
        secs = int(elapsed) % 60
        if self._timer_label and self._timer_label.winfo_exists():
            self._timer_label.config(text=f"{mins}:{secs:02d}")
        self._tick_id = self.after(1000, self._tick)


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    app = CrosswordApp()
    app.mainloop()


if __name__ == "__main__":
    main()
