
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

- [watsonx.ai](https://www.ibm.com/products/watsonx-ai) - WHERE AND HOW THIS IS USED IN OUR SOLUTION

- [watsonx.governance](https://www.ibm.com/products/watsonx-governance) - WHERE AND HOW THIS IS USED IN OUR SOLUTION

- [watsonx Assistant](https://cloud.ibm.com/catalog/services/watsonx-assistant) - WHERE AND HOW THIS IS USED IN OUR SOLUTION

### Other IBM technology used

INSTRUCTIONS: List any other IBM technology or IBM AI services used in your solution and describe how each component was used. If you can provide details on where these were used in your code, that would help the judges review your submission.

**Additional IBM AI services (Remove any that you did not use)**

- [Watson Machine Learning](https://cloud.ibm.com/catalog/services/watson-machine-learning) - WHERE AND HOW THIS IS USED IN OUR SOLUTION

- [Watson Studio](https://cloud.ibm.com/catalog/services/watson-studio) - WHERE AND HOW THIS IS USED IN OUR SOLUTION

- [Natural Language Understanding](https://cloud.ibm.com/catalog/services/natural-language-understanding) - WHERE AND HOW THIS IS USED IN OUR SOLUTION

- [Speech to Text](https://cloud.ibm.com/catalog/services/speech-to-text) - WHERE AND HOW THIS IS USED IN OUR SOLUTION

- [Text to Speech](https://cloud.ibm.com/catalog/services/text-to-speech) - WHERE AND HOW THIS IS USED IN OUR SOLUTION

- [Language Translator](https://cloud.ibm.com/catalog/services/language-translator) - WHERE AND HOW THIS IS USED IN OUR SOLUTION

### Solution architecture

REPLACE THIS EXAMPLE WITH YOUR OWN, OR REMOVE THIS EXAMPLE

Diagram and step-by-step description of the flow of our solution:

![Video transcription/translaftion app](https://developer.ibm.com/developer/tutorials/cfc-starter-kit-speech-to-text-app-example/images/cfc-covid19-remote-education-diagram-2.png)

1. The user navigates to the site and uploads a video file.
2. Watson Speech to Text processes the audio and extracts the text.
3. Watson Translation (optionally) can translate the text to the desired language.
4. The app stores the translated text as a document within Object Storage.

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

You can find a running system to test at...

See our [description document](./docs/DESCRIPTION.md) for log in credentials.

---

_INSTRUCTIONS: You can remove the below section from your specific project README._

## About this template

### Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

### Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

### Authors

<a href="https://github.com/Call-for-Code/Project-Sample/graphs/contributors">
  <img src="https://contributors-img.web.app/image?repo=Call-for-Code/Project-Sample" />
</a>

- **Billie Thompson** - _Initial work_ - [PurpleBooth](https://github.com/PurpleBooth)

### License

This project is licensed under the Apache 2 License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- Based on [Billie Thompson's README template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2).
