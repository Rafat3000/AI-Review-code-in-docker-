# AI-Review-code-in-docker-

# AI Code Review Assistant

This repository contains the source code for **AI Code Review Assistant**, a Streamlit-based web application designed to analyze and review programming code using AI-powered insights. The application supports multiple programming languages and provides feedback on code quality, maintaining a history of reviews for reference.

---

## Features

- **Interactive Sidebar**: View the last five code reviews directly from the sidebar.
- **Multi-language Support**: Select from a list of supported programming languages.
- **Code Review with AI**: Analyze your code quality using AI and receive actionable feedback.
- **Save Review History**: Automatically stores code review data, language, and quality score for future reference.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ai-code-review-assistant.git
2- Navigate to the project directory:
cd ai-code-review-assistant

3- Install the required Python libraries:
pip install -r requirements.txt

4- Create and configure your database (if not pre-configured). You may need to customize the database.py file for your specific database settings.

------------------------

# Usage

1- Run the application:
streamlit run main.py
2- Open the app in your web browser at http://localhost:8501.
3- Use the interface to:
  - Select the programming language.
  - Input your code for review.
  - View the AI-generated review and code quality score.
4- Access recent reviews from the sidebar.

-------

## Project Structure

- main.py: The primary application file containing the Streamlit app logic.
- database.py: Handles database initialization and operations for storing and retrieving reviews.
- ai.py: Contains the AI logic for analyzing and reviewing code.
- utils.py: Utility functions, such as extracting quality scores from AI reviews.
- config.py: Configuration settings, including supported programming languages.

_____

## Requirements

- Python 3.8 or higher
- Streamlit
- Database support (SQLite, MySQL, or similar)
- AI dependencies (specified in requirements.txt)

-------
## Customization

- Add or remove programming languages by editing the PROGRAMMING_LANGUAGES list in config.py.
- Adjust database configurations in database.py to suit your environment.
- Modify the AI logic in ai.py to integrate with different AI models or APIs.

--------
## Contribution

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes.


--------
## License

This project is licensed under the MIT License. See the LICENSE file for details.
