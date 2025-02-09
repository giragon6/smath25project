# Crater Crash

## Inspiration
Over 60% of astronauts experience Spaceflight Associated Neuro-Ocular Syndrome (SANS) [2]. The microgravity environment in space impacts astronauts’ cerebral spinal fluid (CSF) distribution. While in space, excess CSF accumulates in the brain to increase intracranial pressure and cause optic nerve swelling, resulting in blurred vision, difficulty focusing, headaches, and retinal changes. With longer space flight durations, the symptoms worsen. For the safety, comfort, and success of future space missions, finding a solution to SANS is imperative.

## What is Crater Crash?
Crater Crash is an interactive, space-themed visual therapy game designed to reduce and alleviate SANS symptoms for astronauts. Research has shown that visual stimulation induces neural activity, which creates waves of CSF flow in the brain. This flow reduces intracranial pressure and negative symptoms of neuro-ocular syndrome. By playing a fun game, astronauts can maintain their vision for important space missions.

## How We Built It
We used the eyeGestures library, which uses OpenCV under the hood, to track eye movements through an attached web camera. Then, using PyGame, we created a simple brick-breaker game with a few custom assets. By integrating the data recorded from tracking the eyes with the paddle movement controls, we were able to make the paddle move along with the eyes, creating a challenging, visually stimulating game that may help to alleviate SANS symptoms.

## Our Team
This project was built by:
- Caroline D.
- Charlotte G.
- Lily H.
- Emme M.

## Challenges We Faced
We faced a variety of challenges in the process of creating Crater Crash. First, we had trouble narrowing the direction of our solution to SANS, as the problem could be addressed in many aspects, including diagnosis, prevention, and remediation of SANS. After lots of brainstorming (and sticky notes), we based our decision on impact and feasibility. Issues with our code included the inability to transfer the input from the camera to the program, and issues with the game itself. Additionally, we troubleshooted the ball sticking to the paddle and the program crashing once we looked away from the screen.

## Accomplishments We're Proud Of
Our team is proud that we were able to produce the Crater Crash application despite numerous challenges and roadblocks. Additionally, we are proud of the way each member played to their strengths to help the team, while learning new skills and being open to failure. Emme took on OpenCV and the numerous rounds of debugging and iteration associated with a visual-driven program. Caroline used her artistic expertise to design the game interface and compile our engaging product pitch video. Charlotte dove into extensive research on SANS, expanded her experience with Python, and learned new coding extensions. Lily developed our stellar slideshow and contributed to the research aspect. Additionally, she is proud of how the team grew as communicators and collaborators, specifically through an ideation workshop guided by our knowledgeable volunteers.

## What We Learned
We learned a lot about brainstorming and directing our ideas to create feasible solutions. As a team, we learned valuable skills and lessons surrounding coding, perseverance through failure, and the importance of aerospace development. We all gained experience with Github repositories and running lines of code. Though tackling a complex problem in less than 36 hours, we learned to break down a multifaceted issue into manageable and measurable actions.

## What's next for Crater Crash
We plan on modifying the eye tracking algorithm to improve useability and data intake. The game could also use data storage and analysis capabilities to track progression of SANS, as decreased eye movement might indicate decreased cerebral spinal fluid flow. Comparing eye movement capabilities from different flight durations and missions will allow us to better understand the development of spaceflight associated neuro-ocular syndrome. Other options, further into development, include expanding applications to accessible games for disabled individuals, and expanding the game library to include varied digital environments and eye movements.

## Acknowledgements and Resources
A special thanks to the SMathHacks team for their encouragement and support on this project. Also thank you to all volunteers who helped us on this project, from brainstorming to debugging!

Thanks to the open-source OpenCV library eyeGestures! We used their simple_example_v3.py as a base for calibration and eye tracking in our project.

This project was made with the assistance of GitHub Copilot's code completion features.

1. Mehare, A., Chakole, S., & Wandile, B. (2024). Navigating the Unknown: A Comprehensive Review of Spaceflight-Associated Neuro-Ocular Syndrome. Cureus, 16(2), e53380. https://doi.org/10.7759/cureus.53380
2. Williams SD, Setzer B, Fultz NE, Valdiviezo Z, Tacugue N, Diamandis Z, et al. (2023) Neural activity induced by sensory stimulation can drive large-scale cerebrospinal fluid flow during wakefulness in humans. PLoS Biol 21(3): e3002035. https://doi.org/10.1371/journal.pbio.3002035
