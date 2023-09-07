# Clipper

A web clipper application built with Django, which allows users to save and organize web content such as links, articles, and notes.

## Features

- User registration and authentication
- Create, edit, and delete clips
- Add tags to clips for easy organization and filtering
- Search for clips by title, content, URL, or tags

## Installation

To run the application locally:

   ```
   git clone https://github.com/hrbn/clipper.git
   cd clipper
   python -m venv clipper
   source clipper/bin/activate
   pip install -r requirements.txt
   python manage.py makemigrations clipper
   python manage.py migrate
   python manage.py runserver
   ```

Access the application in your browser at `http://localhost:8000`.

## Usage

- Register a new account or log in with an existing account.
- Use the bookmarklet to save web content to your account. Drag the "Save to Clipper" link to your bookmarks bar, then click it on any webpage to save the current selection as a clip.
- Alternatively, you can manually create new clips by clicking the "New Clip" button in the dashboard.
- View and manage your clips in the dashboard. You can edit, delete, and search for clips using the provided filters.
- The tags section on the dashboard displays all the tags used in your clips. Clicking a tag will filter the clips based on that tag.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
