# Product Requirements Document (PRD) for yt-knowledge

## 1. Introduction

### 1.1 Purpose
The yt-knowledge project aims to create a comprehensive knowledge base from YouTube channel subtitles. By downloading, extracting, and optionally translating subtitles from specified channels, the project enables users to access and analyze spoken content in text form.

### 1.2 Scope
This PRD covers the development of a Python/bash-based toolset for:
- Downloading subtitles from YouTube channels
- Extracting and combining subtitle text
- Translating text using external APIs
- Organizing content by channel and format

### 1.3 Target Audience
- Content creators and researchers
- Language learners
- Knowledge management enthusiasts
- Developers interested in YouTube data processing

## 2. Objectives

### 2.1 Business Objectives
- Provide easy access to YouTube content in text format
- Enable multilingual content consumption
- Facilitate content analysis and research

### 2.2 Technical Objectives
- Automate subtitle downloading and processing
- Ensure reliable handling of large datasets
- Maintain data integrity and organization
- Support extensible architecture for future features

## 3. Features

### 3.1 Core Features
- **Channel Subtitle Download**: Download all available English and Hebrew subtitles from specified YouTube channels
- **Text Extraction**: Extract plain text from VTT subtitle files
- **Text Combination**: Merge subtitles from multiple videos into single documents
- **Translation Support**: Translate English text to Hebrew using DeepL API
- **File Organization**: Organize files by channel and type

### 3.2 Advanced Features
- **Resume Downloads**: Continue downloading from where it left off
- **Multiple Format Support**: Handle VTT and SRT subtitle formats
- **Cookie Management**: Support authenticated downloads to bypass restrictions
- **Batch Processing**: Process subtitles in manageable batches

## 4. User Stories

### 4.1 Primary User Stories
1. As a researcher, I want to download all subtitles from an educational YouTube channel so I can analyze the content.
2. As a language learner, I want to translate English subtitles to my native language to improve comprehension.
3. As a content creator, I want to extract text from my videos for SEO and accessibility purposes.

### 4.2 Secondary User Stories
1. As a developer, I want to extend the tool to support other languages and APIs.
2. As a user, I want the tool to handle interruptions gracefully and resume work.

## 5. Requirements

### 5.1 Functional Requirements
- **FR1**: Download subtitles from specified YouTube channels
- **FR2**: Extract text content from subtitle files
- **FR3**: Combine multiple subtitle files into single text documents
- **FR4**: Translate text using external translation services
- **FR5**: Organize files in a structured directory hierarchy

### 5.2 Non-Functional Requirements
- **NFR1**: Process up to 1000 videos per channel
- **NFR2**: Handle timeouts and interruptions gracefully
- **NFR3**: Maintain data integrity during processing
- **NFR4**: Provide clear error messages and logging

### 5.3 Technical Requirements
- **TR1**: Python 3.8+ compatibility
- **TR2**: yt-dlp integration for YouTube access
- **TR3**: DeepL API integration for translation
- **TR4**: Bash scripting for automation
- **TR5**: File system operations for organization

## 6. Technical Specifications

### 6.1 Architecture
- **Scripts Directory**: Contains executable scripts for downloading, extracting, and translating
- **Data Directory**: Stores processed text files and subtitles
- **Channel Directories**: Organized by channel name for easy access

### 6.2 Dependencies
- yt-dlp: For YouTube subtitle downloading
- deepl-python: For translation services
- Python standard library: For file processing

### 6.3 Data Flow
1. User provides channel URL
2. Script fetches video IDs from channel
3. Downloads subtitles for each video
4. Extracts text from subtitle files
5. Combines text into documents
6. Optionally translates to target languages

## 7. User Interface

### 7.1 Command Line Interface
- Bash scripts for automation
- Python scripts for processing
- Clear output messages and progress indicators

### 7.2 Configuration
- Cookie files for authentication
- API keys for translation services
- Configurable batch sizes and delays

## 8. Constraints and Assumptions

### 8.1 Constraints
- Dependent on YouTube's subtitle availability
- Limited by external API rate limits
- Requires valid authentication for restricted content

### 8.2 Assumptions
- Users have access to YouTube content
- External APIs are available and functional
- Sufficient disk space for downloaded content

## 9. Risk Assessment

### 9.1 High Risk
- YouTube API changes affecting downloads
- External service outages
- Large dataset processing timeouts

### 9.2 Mitigation
- Use established libraries (yt-dlp)
- Implement retry mechanisms
- Provide manual intervention options

## 10. Timeline

### 10.1 Phase 1: Core Development (Completed)
- Basic download and extraction functionality

### 10.2 Phase 2: Enhancement (Current)
- Translation integration
- Improved error handling

### 10.3 Phase 3: Optimization (Future)
- Performance improvements
- Additional language support

## 11. Success Metrics

### 11.1 Quantitative
- Number of channels processed
- Amount of text extracted
- Translation accuracy

### 11.2 Qualitative
- User satisfaction
- Ease of use
- Reliability

## 12. Maintenance and Support

### 12.1 Version Control
- Git repository for code management
- Regular updates for dependencies

### 12.2 Documentation
- Comprehensive README
- Inline code comments
- User guides

## 13. Conclusion

The yt-knowledge project provides a robust solution for extracting and processing YouTube subtitle content. By automating the download, extraction, and translation processes, it enables users to create valuable text-based knowledge bases from video content.