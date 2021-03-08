# just a meme to make ashley's day better - replace profanities in code comments with work-safe Gilmore Girls quotes

from profanity_filter import ProfanityFilter
import sys
import os
import random
import re

# stupid shitty list of gilmore quotes
quotes = ["You've got such a great brain!","Because I love you, you idiot!!","I live in two worlds, one is a world of books.","You jump, I jump jack.","I smell snow.","If you're going to throw your life away he better have a motorcycle!!","And if eating cake is wrong, I don't want to be right.","I'm afraid once your heart is involved, it all comes out in moron.","I hate when I'm an idiot and don't know it. I like being aware of my idiocy.","Hey, I have a huge dilemma that I need your opinion on. Am I more beautiful today than yesterday?","Oy with the poodles already!","I had a meeting at the bank earlier, they like callers.","Yeah, I'm fine, I'm great. It's a big, fat, happy sunshine day for me.","God, that's terrible. It's like drinking a My Little Pony.","You gotta realize the only way out is in a body bag.","I'm having nightmares where I'm being chased by boxes with arms and they tackle me and throw clothes on top of me and secure it with masking tape and while I'm lying there, you're standing in the corner laughing putting gel in your hair!","Lorelei, thing where doing here, me, you. I just wanted you to know I'm in, I am all in.","Gnome kicking says a lot about a man's character.","Oh God, I hope nothing's happened to him. You get so attached to their little faces, sometimes you can hear them talk to you at night.","No, it's National Baptism Day. Tie your tubes, idiot!","Rory Gilmore, you should be ashamed of yourself, toying with these boys like this. They used to have pride. They used to have dignity. They used to have balls. Damn it, Gilmore! Give them back their balls!","It's club soda, ace.","You have to tell me why we're committing a felony before we do it.","People are particularly stupid today, I can't talk to any more of them.","Then give me a boa and drive me to rino because I'm open for business!","Well, if you expect that muffin to fly back to the kitchen by itself you better go get it a cape.","You can use your mother's old golf clubs. They're upstairs, gathering dust, with the rest of her potential.","Well, I'll bring dick up on the internet and see what comes up.","Oh, people die, we pay. People crash a car, we pay. People lose a foot, we pay.","Cranking Metallica. Is that some sort of drug reference, it's not funny.","Really? You can see the driveway with your head way up in the air like that?","Why did you drop out of Yale?!","Tell her I gotta take another crack at that closet. I think I hung my Tool t-shirt next to my Metallica t-shirt and they do'nt really get along.","I gotta tell you, out of all the nutty barn raising shindigs this town can cook up, this one wasn't half bad.","Well geez, Ms. Gilmore, why would anyone not want to be in Stars Hollow? That just sounds plumb crazy.","Oh yeah, I've got gold stars plastered all over my forehead.","This town is like one big outpatient mental institution.","Was it because I brought up my meat rub?","If I knew that, I could dismiss my therapist.","I am happy, I'm just sad at the same time. Never been with a woman before?","You thought I'd walk into my daughter's room and get naked?","I wish we had popcorn.","The house is burning, and you can save the cake, or me, what do you choose?","That's not fair, the cake doesn't have legs.","I've got frosted flakes.","He's a grown man with an etch-a sketch!","Shake him real hard, maybe he'll disappear!"]

# creates a filter or some bullshit
pf = ProfanityFilter()

# get the damned filename
filename = sys.argv[1]
file = open(filename)
outfile = open(os.path.splitext(filename)[0] + '-clean' + os.path.splitext(filename)[1], 'w')

def is_comment(line):
    for bit in ['#','%','//','<!--']:
        if(line.startswith(bit)):
            return True
    return False

# fokin loops
for line in file.readlines():

    # if it ain't a comment i don't give a fuck
    if(is_comment(line)):
        line = pf.censor(line)

    line = re.sub('\*\*+', ('"'+quotes[random.randint(0, len(quotes)-1)]+'"').upper(), line)

    outfile.write(line)

file.close()
outfile.close()
