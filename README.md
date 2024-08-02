# Kindle News Aggregator

A program to generate PDFs with news articles, based on user inputs.

## Description

In 2023, Amazon stopped selling new subscriptions of Print and Kindle magazines and newspapers. Whereas staying updated was once painless on the Kindle, it is now no different from browsing the news on your phone or tablet.

This project uses the [News API](https://newsapi.org/) and user prompts to generate a query, returning a PDF with hyperlinks for the user's viewing. The user can read this PDF on their Kindle.

Demo video: [link to demo video]

## Table of Contents

- [Description](#description)
- [Usage](#usage)
- [Future](#future)
- [License](#license)
- [Latest Update](#latest-update)

## Usage

To use this program, you need to generate an API key with the [News API](https://newsapi.org/). Paste this key and the absolute path of your destination folder for the PDF into the configuration file, and run the driver (`news.py`).

The program uses a CLI (command-line interface). When prompted to enter information, the user can choose whether or not to include it. Note that if no parameters are provided, the News API will not run, as there would be too much information to return. Consequently, the program will not run.

## Future

- **Error Validation**: Implement thorough error validation to handle various edge cases.
- **MongoDB Integration**: Ensure additional PDFs don't include the same content as prior ones. MongoDB will make working with JSONs easier, allowing for seamless serialization of news information.
- **Advanced Queries**: Add more filters to generate advanced queries. This might change JSON representations, but MongoDB will facilitate these changes seamlessly.
- **Additional APIs**: Integrate more news-related APIs for wider news coverage.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Latest Update

- Added support for generating PDFs with hyperlinks.
- Improved CLI for user input.
