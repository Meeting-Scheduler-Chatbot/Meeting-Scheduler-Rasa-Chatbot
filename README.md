
# Meeting Scheduler Chatbot

Scheduling a meeting is a really time-consuming task. We are planning to make this process easier by developing a chatbot with a special scheduling algorithm which is based on participants calendar information that we will access by authenticating users calendars. This way users will not suffer because of the looping mail traffic while arranging meetings and they can focus on their tasks. We decided to develop a chatbot since we can integrate it with the tools that are used in the industry, such as Slack or Microsoft Teams.

To develop a chatbot we should, we decided to use Natural Language Understanding (NLU) methods instead of the state machine approach, in order to increase user experience. We are going to use NLU to under- stand the intent of the user to make the conversation more likely to human-human conversations. Our goal is to give the feeling to the user that they are talking with a real assistant. Besides the chatbot part of this project, we also need create database in order to manage user information.

Also, a website is required to register users, authenticate their calendars, and manage their meeting groups. Therefore, a lot of information transaction happens between database, website, and chatbot. Since we will store the user’s personal data and authenticate keys, we will manage security between database and chatbot by analyzing possible vulnerabilities of system. 

In the end of the project, a flow is created such that a user can register the website, authenticate his/her calendar, create a meeting group, and then go to Google’s Hangout Chat, from app market can add the bot and arrange a meeting. After that, the participants of the meeting are receives an email and can see the event in their calendars with the related name and duration.

# README Contents
1. [Authors](#authors)
2. [Tech Stack](#tech-stack)
3. [Deliverables](#deliverables)
4. [How to Run Docker](#how-to-run-docker)
5. [How to Deploy](#how-to-deploy)
6. [Screenshots](#screenshots)
    - [Flow](#flow)
    - [Dashboard](#dashboard)
    - [Example Conversations](#example-conversations)
    - [Analyzer](#analyzer)
    - [Scheduling Algorithm Explained](#scheduling-algorithm-explained)
    - [Scheduling Algorithm Timing Graphs](#scheduling-algorithm-timing-graphs)
8. [Feedback](#feedback)

## Authors
- [@cavitcakir](https://www.github.com/cavitcakir)
- [@kayakapagan](https://www.github.com/kayakapagan)
- [@gokberkyar (contributor)](https://www.github.com/gokberkyar)

## Tech Stack

**Frontend:** React, Redux, Material UI

**Backend:** Node.js, Express.js

**Database:** MongoDB

**Testing:** NodeJsScan

**Other:** Docker

<p align="center">
    <code><img height="40" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/icons/react-logo.png"></code>
    <code><img height="40" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/icons/redux-logo.png"></code>
    <code><img height="40" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/icons/materialUI-logo.png"></code>
    <code><img height="40" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/icons/node-logo.jpeg"></code>
    <code><img height="40" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/icons/express-logo.jpeg"></code>
    <code><img height="40" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/icons/mongo-logo.png"></code>
    <code><img height="40" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/icons/nodejsscan-logo.png"></code>
    <code><img height="40" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/icons/docker-logo.png"></code>

</p>

## Deliverables
   - [report](https://github.com/Meeting-Scheduler-Chatbot/website/blob/main/website-images/ens491.pdf)
   - [presentation](https://github.com/Meeting-Scheduler-Chatbot/website/blob/main/website-images/ENS492%20Presentation.pdf)
   - [chart](https://lucid.app/publicSegments/view/f1aacb7a-91e0-4d8b-af27-bda16af04d4e/image.png)

## How to Run Docker
```shell
docker-compose -f docker-compose.dev.yml up
```

## How to Deploy
  - [read this file](https://docs.google.com/document/d/15DVsJrgqgdd-DC_xgbWGQWcOPiM9pKXTopugIjup2rI/edit?usp=sharing)

## Screenshots

### Flow
<div align="center">
<img   src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/flow.png"/>
</div>


### Dashboard
<div align="center">
<img   src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/front-end-images/page_signup.png"/>
<img   src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/front-end-images/page_signin.png"/>
<img   src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/front-end-images/page_settings.png"/>
<img   src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/front-end-images/page_my_groups.png"/>
<img   src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/front-end-images/page_group_edit.png"/>
<img   src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/front-end-images/page_add_group.png"/>
<img   src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/front-end-images/google_auth.png"/> 
</div>


### Example Conversations
<div align="center">
<img   src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/example_slack_conv.png"/>
<img   src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/google-chat-conv.png"/>
</div>

### Analyzer
<div align="center"> 
<img  src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/analyzer_2.png"/>
</div>


### Scheduling Algorithm Explained
<div align="center">
<img  src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/Scheduling_Algorithm_Chart.png"/>
</div>

### Scheduling Algorithm Timing Graphs
<div align="center" > 
<img  height="220" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/schedule_algorithm_timing_figures/Figure_1.png"/>
<img  height="220" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/schedule_algorithm_timing_figures/Figure_2.png"/>
<img  height="220" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/schedule_algorithm_timing_figures/Figure_3.png"/>
<img height="220" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/schedule_algorithm_timing_figures/Figure_4.png"/>
<img height="220" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/schedule_algorithm_timing_figures/Figure_5.png"/>
<img height="220" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/schedule_algorithm_timing_figures/Figure_6.png"/>
<img height="220" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/schedule_algorithm_timing_figures/Figure_7.png"/>
<img height="220" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/schedule_algorithm_timing_figures/Figure_8.png"/>
<img height="220" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/schedule_algorithm_timing_figures/Figure_9.png"/>
<img  height="220" src="https://raw.githubusercontent.com/Meeting-Scheduler-Chatbot/website/main/website-images/schedule_algorithm_timing_figures/Figure_10.png"/>
</div>

## Feedback
Feel free to create an issue to discuss more.
