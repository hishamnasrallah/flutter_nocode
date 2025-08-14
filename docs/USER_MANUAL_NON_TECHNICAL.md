# Flutter App Builder - User Manual for Non-Technical Users

Welcome to Flutter App Builder! This guide will help you create your own mobile applications without any programming knowledge.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Creating Your First App](#creating-your-first-app)
3. [Designing Your App's Look](#designing-your-apps-look)
4. [Adding Screens to Your App](#adding-screens-to-your-app)
5. [Adding Content and Buttons](#adding-content-and-buttons)
6. [Connecting to Data Sources](#connecting-to-data-sources)
7. [Creating Actions (What Happens When Users Tap)](#creating-actions)
8. [Building Your App](#building-your-app)
9. [Troubleshooting](#troubleshooting)

## Getting Started

### What is Flutter App Builder?
Flutter App Builder is a tool that lets you create mobile applications for Android phones without writing any code. You simply use a web interface to design your app, add content, and configure how it works.

### Accessing the System
1. Open your web browser
2. Go to the Flutter App Builder website
3. Log in with your username and password
4. You'll see the main dashboard with different sections

## Creating Your First App

### Step 1: Create a New Application
1. Click on "Flutter Applications" in the main menu
2. Click the "Add Flutter Application" button
3. Fill in the following information:
   - **App Name**: What your app will be called (e.g., "My Store App")
   - **App Description**: A brief description of what your app does
   - **Package Identifier**: A unique identifier (use format: com.yourname.appname)
   - **App Version**: Start with "1.0.0"
   - **App Theme**: Choose a color scheme (you can create themes in the "App Themes" section)

### Step 2: Save Your Application
1. Click "Save" to create your application
2. You'll see your new app in the applications list

## Designing Your App's Look

### Creating a Theme
1. Go to "App Themes" in the main menu
2. Click "Add App Theme"
3. Configure your theme:
   - **Theme Name**: Give it a descriptive name (e.g., "Blue Ocean Theme")
   - **Main Color**: The primary color for buttons and headers
   - **Accent Color**: Secondary color for highlights
   - **Background Color**: Main background color
   - **Text Color**: Default text color
   - **Font Style**: Choose a font family
   - **Dark Mode**: Enable if you want a dark theme

### Applying a Theme to Your App
1. Go back to your application
2. Edit the application
3. Select your theme from the "App Theme" dropdown
4. Save the changes

## Adding Screens to Your App

### What are Screens?
Screens are like pages in your app. For example, you might have a "Home" screen, a "Products" screen, and a "Contact" screen.

### Creating a Screen
1. Open your application for editing
2. Scroll down to the "App Screens" section
3. Click "Add another App Screen"
4. Fill in the screen information:
   - **Screen Name**: Descriptive name (e.g., "Home Page")
   - **Screen Route**: Internal name starting with "/" (e.g., "/home")
   - **Home Screen**: Check this for your main screen
   - **Top Bar Title**: Text shown at the top of the screen
   - **Show Top Bar**: Whether to show the title bar
   - **Show Back Button**: Whether users can go back

### Screen Types You Might Create
- **Home Screen**: The first screen users see
- **Product List**: Shows your products or services
- **Contact Screen**: Your contact information
- **About Screen**: Information about your business

## Adding Content and Buttons

### What are Widgets?
Widgets are the building blocks of your app - things like text, images, buttons, and lists.

### Adding Widgets to a Screen
1. Go to "Widgets" in the main menu
2. Click "Add Widget"
3. Choose your screen from the dropdown
4. Select a widget type:
   - **Text**: For displaying text
   - **Image**: For showing pictures
   - **Raised Button**: For clickable buttons
   - **Vertical Layout (Column)**: To stack items vertically
   - **Horizontal Layout (Row)**: To arrange items side by side
   - **Scrollable List**: For lists of items

### Configuring Widget Properties
After creating a widget, you need to set its properties:

1. Go to the widget you just created
2. Scroll down to "Widget Properties"
3. Add properties based on your widget type:

#### For Text Widgets:
- **Property Name**: "text"
- **Property Type**: "Text"
- **Text Value**: Enter your text

#### For Button Widgets:
- **Property Name**: "text"
- **Property Type**: "Text"
- **Text Value**: Button text (e.g., "Click Me")

#### For Image Widgets:
- **Property Name**: "imageUrl"
- **Property Type**: "Web Address"
- **URL Value**: Link to your image

### Organizing Widgets
- Use **Display Order** to control the sequence of widgets
- Use **Parent Widget** to put widgets inside containers
- Use **Container** widgets to group related items

## Connecting to Data Sources

### What are Data Sources?
Data sources provide dynamic content for your app, like product lists, news articles, or user information.

### Creating a Data Source
1. Go to "Data Sources" in the main menu
2. Click "Add Data Source"
3. Fill in the information:
   - **Application**: Select your app
   - **Data Source Name**: Descriptive name (e.g., "Product List")
   - **Data Source Type**: Choose "REST API" for web services or "Static JSON Data" for fixed data
   - **API Base URL**: The main web address (e.g., "https://api.mystore.com")
   - **API Endpoint**: The specific path (e.g., "/products")
   - **Request Method**: Usually "GET (Retrieve Data)"

### Defining Data Fields
After creating a data source, define what information it provides:

1. In your data source, scroll to "Data Fields"
2. Add fields for each piece of information:
   - **Field Name**: Internal name (e.g., "product_name")
   - **Field Type**: Type of data (Text, Number, Image Web Address, etc.)
   - **Display Name**: Human-readable name (e.g., "Product Name")
   - **Required Field**: Check if this field is always present

### Using Data in Widgets
1. Create a widget (like a List or Text)
2. Add a property with type "Data Field"
3. Select the data field you want to display

## Creating Actions (What Happens When Users Tap)

### What are Actions?
Actions define what happens when users interact with your app, like tapping a button or selecting an item.

### Creating an Action
1. Go to "Actions" in the main menu
2. Click "Add Action"
3. Configure the action:
   - **Application**: Select your app
   - **Action Name**: Descriptive name (e.g., "Go to Product Details")
   - **Action Type**: Choose what should happen:
     - **Navigate to Screen**: Go to another screen
     - **Show Popup Message**: Display a message
     - **Call Web Service**: Get data from the internet
     - **Open Web Page**: Open a website
     - **Send Email**: Open email app

### Common Action Types

#### Navigation Actions
- **Target Screen**: Choose which screen to open
- Use for: Menu buttons, "Learn More" buttons

#### Popup Messages
- **Dialog Title**: Title of the popup
- **Dialog Message**: Message content
- Use for: Confirmations, alerts, information

#### Web Service Calls
- **API Data Source**: Choose your data source
- Use for: Loading data, submitting forms

### Connecting Actions to Widgets
1. Edit a widget (like a button)
2. Add a property:
   - **Property Name**: "onPressed"
   - **Property Type**: "Action (What Happens)"
   - **Action Reference**: Select your action

## Building Your App

### Generating Your App
1. Go to your application in "Flutter Applications"
2. Select your application
3. From the "Action" dropdown, choose "🔧 Generate Flutter Source Code"
4. Click "Go" - this creates the app code

### Building the APK File
1. After generating code, select your application again
2. From the "Action" dropdown, choose "📱 Build APK File"
3. Click "Go" - this creates the installable app file
4. Wait for the build to complete (this may take several minutes)

### Downloading Your App
1. Open your application for editing
2. Scroll down to "Generated Files"
3. Click on the APK file link to download your app
4. You can also download the source code ZIP file

### Installing Your App
1. Transfer the APK file to your Android phone
2. Enable "Install from Unknown Sources" in your phone's settings
3. Tap the APK file to install your app

## Sample Applications

### Quick Start with Samples
To learn how the system works, you can create sample applications:

1. Create a new application
2. Select it in the applications list
3. Choose one of these actions:
   - **🛒 Create E-commerce Sample**: Creates a shopping app
   - **📱 Create Social Media Sample**: Creates a social networking app
   - **📰 Create News App Sample**: Creates a news reading app

These samples show you how complex apps are structured and give you ideas for your own projects.

## Troubleshooting

### Common Issues

#### "Build Failed" Error
- Check that all required fields are filled in
- Make sure your data sources are working
- Verify that all actions have proper targets

#### App Crashes on Phone
- Ensure all required widget properties are set
- Check that data source URLs are correct
- Verify that all screens have content

#### Can't Download APK
- Make sure the build completed successfully
- Check the build history for error messages
- Try building again if the first attempt failed

### Getting Help

#### Build History
- Check "Build History" to see detailed logs
- Look for error messages that explain what went wrong
- Each build attempt is recorded with timestamps

#### Testing Your App
- Always test your app on a real device
- Try all buttons and navigation
- Check that data loads correctly

### Best Practices

#### Planning Your App
1. Sketch your app screens on paper first
2. List what content each screen needs
3. Plan how users will navigate between screens

#### Organizing Your Work
1. Create themes before building screens
2. Set up data sources before creating lists
3. Test frequently by building and installing

#### Naming Conventions
- Use clear, descriptive names for everything
- Keep screen routes simple (e.g., "/home", "/products")
- Use consistent naming across your app

## Advanced Features

### Custom Widgets from pub.dev
You can add advanced widgets from the Flutter community:

1. Go to "Custom Widgets (pub.dev)" in your application
2. Add the package name and widget class
3. The widget will be available when generating your app

### Multiple Data Sources
You can connect to multiple APIs:
- Product catalog from one service
- User reviews from another
- Payment processing from a third service

### Complex Navigation
Create sophisticated navigation patterns:
- Tab bars at the bottom
- Side menus (drawers)
- Multi-level navigation

Remember: This tool is designed to be user-friendly. Don't be afraid to experiment and try different configurations. You can always create new test applications to practice with!