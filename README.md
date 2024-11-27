# Verblaze

Verblaze is an automatic localization generation tool that helps you manage and generate translations for your projects.

📚 **[Visit verblaze.com](https://verblaze.com)** for detailed guides and examples.

## Features

- 🚀 Quick and easy setup
- 🌍 Support for multiple frameworks and technologies
- 📦 Automatic string extraction
- 🔄 Seamless integration with Verblaze Dashboard
- 💻 Simple command-line interface

## Installation

```bash
pip install verblaze
```

## Quick Start

### 1. Configure Verblaze

First, set up your Verblaze configuration using your secret key from the dashboard:

```bash
verblaze config --secret-key YOUR_SECRET_KEY
```

### 2. Generate Translations

Extract strings from your project using the generate command:

```bash
verblaze generate -t TEMPLATE -d PROJECT_DIRECTORY -f FOLDERS
```

#### Parameters:

- `-t`: Template/framework (Required)
  - Supported templates: flutter, react, react-native, angular, plain-html, vue, svelte, ember, backbone, swift, kotlin, javafx, wpf, qt, blazor, nextjs
- `-d`: Project directory path (Required)
- `-f`: Folders containing UI code, comma-separated (Required)

#### Example:

```bash
verblaze generate -t react -d /path/to/project -f "src,components,pages"
```

## Supported Frameworks

- React
- React Native
- Angular
- Vue
- Svelte
- Flutter
- Plain HTML
- Ember
- Backbone
- Swift
- Kotlin
- JavaFX
- WPF
- Qt
- Blazor
- Next.js

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

- Website: [verblaze.com](https://verblaze.com)
- Email: support@verblaze.com
- [Github](https://github.com/Verblaze)

## FAQ

**Q: How do I get my secret key?**
A: You can obtain your secret key from the Verblaze Dashboard after creating an account.

**Q: Which Python versions are supported?**
A: Python 3.6 and above are supported.

**Q: Can I use Verblaze with my existing project?**
A: Yes, Verblaze supports multiple frameworks and can be integrated with existing projects.

## Changelog

### [0.0.1] - 2024-11-20

- Initial release
- Added support for multiple frameworks
- Implemented string extraction functionality
- Created CLI interface with config and generate commands
