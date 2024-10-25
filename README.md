
# SuperNova/VITA

- [Project summary](#project-summary)
  - [The issue we are hoping to solve](#the-issue-we-are-hoping-to-solve)
  - [How our technology solution can help](#how-our-technology-solution-can-help)
  - [Our idea](#our-idea)
- [Technology implementation](#technology-implementation)
  - [IBM watsonx product(s) used](#ibm-ai-services-used)
  - [Other IBM technology used](#other-ibm-technology-used)
  - [Solution architecture](#solution-architecture)
- [Presentation materials](#presentation-materials)
  - [Solution demo video](#solution-demo-video)
  - [Project development roadmap](#project-development-roadmap)
- [Additional details](#additional-details)
  - [How to run the project](#how-to-run-the-project)
  - [Live demo](#live-demo)
- [About this template](#about-this-template)
  - [Contributing](#contributing)
  - [Versioning](#versioning)
  - [Authors](#authors)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)



## Project summary

### The issue we are hoping to solve
Limited healthcare accessibility in communities, particularly rural areas, has become a critical issue. These areas need more doctors and medical practitioners, making it difficult for residents to receive timely and effective medical care.


### How our technology solution can help

We developed a web application allowing users to upload images and describe their symptoms, providing a diagnosis and treatment suggestions.

### Our idea

Our solution, a pioneering AI-powered web application, seeks to revolutionize healthcare accessibility in all communities, especially rural communities. Recognizing the critical shortage of doctors and skilled medical practitioners in these areas, we have developed a technology that leverages artificial intelligence to provide timely medical advice and support to individuals who lack easy access to healthcare facilities.

Despite progress in digital healthcare, there's still a lack of research on at-home treatment suggestion systems. While some platforms offer remote consultations, none provide personalized treatment options based on user-uploaded images and descriptions. Filling this gap presents a chance to develop a unique solution for people seeking care. Using a technological solution, we aim to address this gap.

At the heart of our solution lies a user-friendly web app interface accessible via smartphones or computers. This interface allows users to interact with the system by either uploading images of their medical issues and inputting descriptions of their symptoms, ensuring that individuals with varying levels of technological proficiency can easily utilize the service.

The process begins when a user initiates a conversation with the chatbot, typically by uploading images of their medical condition. The chatbot employs three convolutional neural networks (CNNs) to enhance accuracy. Our main classification model GoogleLeNet, boasting an accuracy of 86.22%, analyses the images to identify key features and patterns indicative of specific medical conditions. Additionally, two supporting CNNs — image enhancement (U-Net) and light adjustment models (CIDNet) — further refine the images, ensuring that diagnostic accuracy remains high. This multi-layered approach guarantees the best possible analysis regardless of the quality or condition of the uploaded images.

Simultaneously, we utilize text inputs to gather insight into user symptoms. Once the user's input is processed, a rule-based system provides the user with valid treatment suggestions. Additionally, the web app incorporates Retrieval-Augmented Generation (RAG) to continuously provide the most up-to-date and relevant information using natural language processing (NLP) to understand and answer user concerns. The chatbot consults a vast database created in collaboration with healthcare practitioners and medical journals to ensure accurate responses. 

Our solution also has multilingual capabilities and cross-device compatibility, ensuring it reaches diverse populations with ease. The chatbot's responses are designed to be both informative and actionable. For straightforward, non-urgent cases, it may offer self-care advice or recommend over-the-counter medications. In more serious cases, the chatbot advises users to seek medical attention from a healthcare practitioner.
Additionally, the web app provides users with the ability to revisit their previous consultations. This feature enables users to easily access a detailed history of their past interactions with the system, including the treatment suggestions they received during those consultations. This feature empowers users and healthcare practitioners to make informed decisions about their health based on their treatment history.

In summary, our AI-powered web app represents a groundbreaking solution to healthcare access challenges. By harnessing artificial intelligence, including CNN models, machine learning, RAG, multilingual capabilities, and more, we empower individuals to manage their health and well-being regardless of geographic location or access to traditional healthcare facilities.


More detail is available in our [description document](./docs/DESCRIPTION.md).

## Technology implementation

### IBM watsonx product(s) used

_INSTRUCTIONS: Included here is a list of IBM watsonx products. Remove any products you did not use. Leave only those included in your solution code. In your official submission on the Call for Code Global Challenge web site, you are required to provide details on where and how you used each IBM watsonx product so judges can review your implementation. Remove these instructions._

**Featured watsonx products**



- [watsonx Assistant](https://cloud.ibm.com/catalog/services/watsonx-assistant) -  In VITA, Watsonx Assistant is central to user engagement, providing a conversational interface for users to interact with the system. One of its key roles is in conducting severity analysis through a rule-based system. This system operates by analyzing the user's initial responses to health-related queries, applying predefined medical guidelines, and decision rules to assess the severity of symptoms. Factors such as symptom duration, intensity, and risk indicators are processed to categorize the condition as mild, moderate, or critical. This allows VITA to determine the urgency of a user's condition.
In addition to severity analysis, VITA allows users to ask follow-up or additional questions beyond the initial assessment. For these more complex or detailed inquiries, Retrieval-Augmented Generation (RAG) is employed. Watsonx Machine Learning retrieves relevant information from a curated medical knowledge base and generates accurate, contextually relevant responses to users' questions. This ensures that users can receive comprehensive answers to specific medical concerns, enhancing the user experience by providing both rule-based assessments and AI-generated insights.
By combining a rule-based severity analysis system with RAG for additional queries, Watsonx Assistant in VITA offers a robust and versatile health support system, ensuring both quick triage for urgent cases and detailed, data-driven responses for broader medical inquiries.
**1. Main Diagnostic Assistant (New Chat Template)**: On the dedicated New Chat Template, Watsonx Assistant is responsible for handling the core diagnostic functions, including severity analysis. This assistant collects user input regarding symptoms, health concerns, and other relevant data. The assistant uses a rule-based system to analyze the severity of the symptoms by comparing them to predefined medical guidelines and thresholds. 

**2. Helper Assistant (All Other Templates)**: The second instance of Watsonx Assistant is a web app assistant, available on all templates except the New Chat template. This assistant is designed to guide users through the functionality of the VITA web application. It helps users understand how to navigate the platform, how to start new conversations with the diagnostic assistant, and how to access other features such as reviewing past interactions, managing their profile, or using other tools within the system. This assistant enhances the user experience by providing clear and immediate assistance on how to use the web application effectively, ensuring a seamless user journey with VITA.

### Other IBM technology used


- [Watson Machine Learning](https://cloud.ibm.com/catalog/services/watson-machine-learning) - In VITA, Watson Machine Learning is integral to the platform's intelligent response system, specifically supporting the Retrieval-Augmented Generation (RAG) model. This technology is deployed in the Main Diagnostic Assistant on the New Chat Page to enhance the system’s ability to generate precise, data-driven medical guidance. When a user interacts with the diagnostic assistant—especially after the initial rule-based severity analysis—Watson Machine Learning processes the user's input and retrieves the most relevant information from a curated medical knowledge base.
The RAG model is responsible for fetching up-to-date, accurate data from this knowledge base and generating responses that are tailored to the user's specific health inquiry. For example, if a user asks about possible treatments for a diagnosed condition or requests further clarification on their symptoms, the RAG model provides real-time, context-aware answers based on the latest medical research and guidelines. This allows VITA to offer not only diagnostic assessments but also actionable and informed recommendations that are personalized to the user’s needs.


- [Watson Studio](https://cloud.ibm.com/catalog/services/watson-studio) - Watson Studio serves as the comprehensive development platform for VITA, hosting all Watson services within a unified environment. It acts as the backbone of the platform, streamlining the entire workflow. By centralizing these critical functions, Watson Studio enables our team to efficiently manage and oversee all AI components powering VITA.
In addition, Watson Studio ensures that all components—from the assistants to the underlying AI systems—are deployed in a scalable and optimized manner. This seamless integration of all Watson services within a single environment ensures that VITA delivers reliable, real-time medical insights to users, while maintaining high performance and reducing the complexity of managing multiple AI components.


- [Text to Speech](https://cloud.ibm.com/catalog/services/text-to-speech) - In VITA, the Text-to-Speech (TTS) functionality is used to convert written documentation into audio files, which describe our services and the app. These audio files are available in the platform's documentation, allowing users to listen to articles and informational content that explain how VITA works, its features, and the services it provides. By offering audio for these documents, VITA ensures that users who prefer or need an audio-based experience can engage with the content without having to read through the text.
This feature enhances accessibility, catering to users with visual impairments or those who find it more convenient to listen rather than read. It allows users to easily consume information about VITA's medical tools, diagnosis processes, and AI-driven features while multitasking or when reading is not feasible. By using TTS, VITA ensures a more inclusive user experience, making the platform's key informational resources available to a broader audience through spoken word.

- [Jupyter Notebook Editor (within Watson Studio)](https://developer.ibm.com/components/jupyter/) - In VITA, the Jupyter Notebook Editor within Watson Studio is specifically used to train the classification models that support the platform’s health analysis features. These classification models are critical for analyzing user inputs and accurately determining the severity of symptoms or categorizing health conditions. 


### Solution architecture

Diagram and step-by-step description of the flow of our solution:

![Vita _app](https://drive.usercontent.google.com/download?id=1FxTiz0E5y6oB66PCXtLNG7Y1kuNc70Cd&export=view&authuser=0)

**1. User Registration/Login & Navigation:** Users can register or log in to the site. Upon registration, the user’s details are automatically updated in the database. After login, users can navigate the site seamlessly.
**2. Image Upload & Disease Classification:** Users upload an image of a disease, which is processed by a machine learning model. The model enhances the image if necessary and classifies the disease.
**3. Integration with Watsonx Assistant:** The classification result is sent to the Watsonx Assistant chatbot, which initiates an interaction with the user based on the disease classification.
**4. Chatbot Analysis & Treatment Recommendations:** Watsonx Assistant asks relevant questions to assess the severity of the condition and provides treatment suggestions based on the responses.
**5. Machine Learning-Powered Answers:** If the user has additional questions, watsonx’s machine learning capabilities are utilized to generate accurate answers.
**6. Data Storage & Accessibility:** The entire conversation, including the uploaded image and classification details, is saved in the database. Users can view this information at any time.

## Presentation materials

_INSTRUCTIONS: The following deliverables should be officially posted to your My Team > Submissions section of the [Call for Code Global Challenge resources site](https://cfc-prod.skillsnetwork.site/), but you can also include them here for completeness. Replace the examples seen here with your own deliverable links._

### Solution demo video

[![Watch the video](https://raw.githubusercontent.com/Liquid-Prep/Liquid-Prep/main/images/readme/IBM-interview-video-image.png)](https://youtu.be/vOgCOoy_Bx0)

### Project development roadmap

The project currently does the following things.

- Feature 1
- Feature 2
- Feature 3

In the future we plan to...

See below for our proposed schedule on next steps after Call for Code 2024 submission.

![Roadmap](./images/roadmap.jpg)

## Additional details

_INSTRUCTIONS: The following deliverables are suggested, but **optional**. Additional details like this can help the judges better review your solution. Remove any sections you are not using._

### How to run the project

INSTRUCTIONS: In this section you add the instructions to run your project on your local machine for development and testing purposes. You can also add instructions on how to deploy the project in production.

### Live demo

You can find a running app at [description document](./docs/DESCRIPTION.md)





### Authors

<a href="https://github.com/Call-for-Code/Project-Sample/graphs/contributors">
  <img src="https://contributors-img.web.app/image?repo=Call-for-Code/Project-Sample" />
</a>
s.

