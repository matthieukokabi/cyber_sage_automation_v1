# Cyber Sage Chronicles - Product Requirements Document (PRD)

## 📋 Project Overview

**Project Name:** Cyber Sage Chronicles  
**Version:** 1.0  
**Last Updated:** January 22, 2026  
**Author:** Matthieu Kokabi  
**Status:** In Development

### Vision Statement
Create a fully automated YouTube Shorts content factory powered by AI that generates, produces, and publishes cyberpunk-themed educational and storytelling content with minimal human intervention.

---

## 🎯 Objectives

### Primary Goals
1. Automate the entire content creation pipeline from topic input to video publication
2. 2. Generate engaging, viral-worthy YouTube Shorts (60 seconds max)
   3. 3. Maintain a consistent cyberpunk/futuristic aesthetic across all content
      4. 4. Minimize manual intervention to less than 5 minutes per video
        
         5. ### Success Metrics
         6. - Video generation time: < 10 minutes per Short
            - - Content quality score: 4+ stars user rating
              - - Upload automation: 100% hands-free publishing
                - - Daily output capacity: 3-5 videos per day
                 
                  - ---

                  ## 🏗️ System Architecture

                  ### High-Level Architecture

                  ```
                  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
                  │    TELEGRAM     │────▶│   PYTHON BOT    │────▶│    MAKE.COM     │
                  │    (Frontend)   │     │  (Middleware)   │     │   (Backend)     │
                  └─────────────────┘     └─────────────────┘     └─────────────────┘
                          │                       │                       │
                          │                       ▼                       ▼
                          │               ┌─────────────────┐     ┌─────────────────┐
                          │               │   GEMINI AI     │     │  VIDEO TOOLS    │
                          │               │ (Content Gen)   │     │   (Production)  │
                          │               └─────────────────┘     └─────────────────┘
                          │                                               │
                          │                                               ▼
                          │                                       ┌─────────────────┐
                          └──────────────────────────────────────▶│    YOUTUBE      │
                                     Feedback Loop                │   (Publishing)  │
                                                                  └─────────────────┘
                  ```

                  ### Component Details

                  #### 1. Frontend Layer - Telegram Bot
                  - **Purpose:** User interface for topic input and status monitoring
                  - - **Technology:** Telegram Bot API
                    - - **Bot Name:** Pip v2 (Gemini-Powered)
                      - - **Commands:**
                        -   - `/start` - Initialize bot connection
                            -   - Text messages - Submit topics for content generation
                             
                                - #### 2. Middleware Layer - Python Bot
                                - - **Purpose:** Orchestrate AI generation and webhook communication
                                  - - **Technology:** Python 3.x, python-telegram-bot, google-generativeai
                                    - - **Location:** `/src/bot.py`
                                      - - **Responsibilities:**
                                        -   - Receive Telegram messages
                                            -   - Call Gemini AI for content generation
                                                -   - Format and transmit payload to Make.com
                                                    -   - Provide user feedback
                                                     
                                                        - #### 3. AI Layer - Google Gemini
                                                        - - **Purpose:** Generate scripts and visual prompts
                                                          - - **Model:** gemini-1.5-flash
                                                            - - **Outputs:**
                                                              -   - Narration script (130-150 words, ~60 seconds)
                                                                  -   - Visual prompt for image generation (Midjourney/Flux compatible)
                                                                   
                                                                      - #### 4. Backend Layer - Make.com
                                                                      - - **Purpose:** Automate video production and publishing workflow
                                                                        - - **Current Status:** Webhook configured (Pip Uplink)
                                                                          - - **Webhook URL:** `https://hook.eu1.make.com/wg9ih5bmi2myooxgkzixqjmyk734`
                                                                           
                                                                            - ---

                                                                            ## 📦 Data Structures

                                                                            ### Webhook Payload (Bot → Make.com)

                                                                            ```json
                                                                            {
                                                                              "topic": "string - User's topic input",
                                                                              "script": "string - Generated narration script",
                                                                              "visual_prompt": "string - Image generation prompt",
                                                                              "user_id": "integer - Telegram user ID",
                                                                              "timestamp": "string - ISO 8601 timestamp",
                                                                              "settings": {
                                                                                "style": "Cinematic Cyberpunk",
                                                                                "duration": "60s",
                                                                                "platform": "YouTube Shorts",
                                                                                "narrative_mode": "Storytelling"
                                                                              }
                                                                            }
                                                                            ```

                                                                            ---

                                                                            ## 🔧 Technical Requirements

                                                                            ### Dependencies (requirements.txt)
                                                                            ```
                                                                            python-telegram-bot>=20.0
                                                                            python-dotenv
                                                                            requests
                                                                            google-generativeai
                                                                            ```

                                                                            ### Environment Variables (.env)
                                                                            ```
                                                                            TELEGRAM_TOKEN=your_telegram_bot_token
                                                                            MAKE_WEBHOOK_URL=your_make_webhook_url
                                                                            GEMINI_API_KEY=your_gemini_api_key
                                                                            ```

                                                                            ---

                                                                            ## 🔄 Workflow Pipeline

                                                                            ### Current Implementation (Phase 1)

                                                                            ```
                                                                            1. User sends topic via Telegram
                                                                                   ↓
                                                                            2. Bot receives and validates input
                                                                                   ↓
                                                                            3. Gemini AI generates script + visual prompt
                                                                                   ↓
                                                                            4. Bot sends enriched payload to Make.com webhook
                                                                                   ↓
                                                                            5. User receives confirmation with preview
                                                                            ```

                                                                            ### Planned Implementation (Phase 2+)

                                                                            ```
                                                                            6. Make.com triggers image generation (Midjourney/Flux)
                                                                                   ↓
                                                                            7. Make.com triggers audio generation (ElevenLabs/TTS)
                                                                                   ↓
                                                                            8. Make.com triggers video assembly (Creatomate/Shotstack)
                                                                                   ↓
                                                                            9. Make.com triggers video upload (YouTube API)
                                                                                   ↓
                                                                            10. User receives final video link via Telegram
                                                                            ```

                                                                            ---

                                                                            ## 🛠️ API Integrations

                                                                            | Service | Purpose | Status | Priority |
                                                                            |---------|---------|--------|----------|
                                                                            | Telegram Bot API | User Interface | ✅ Implemented | P0 |
                                                                            | Google Gemini | Script Generation | ✅ Implemented | P0 |
                                                                            | Make.com Webhooks | Workflow Automation | ✅ Connected | P0 |
                                                                            | Midjourney/Flux | Image Generation | 🔲 Planned | P1 |
                                                                            | ElevenLabs/TTS | Voice Narration | 🔲 Planned | P1 |
                                                                            | Creatomate/Shotstack | Video Assembly | 🔲 Planned | P1 |
                                                                            | YouTube Data API | Video Publishing | 🔲 Planned | P2 |
                                                                            | Google Drive | Asset Storage | 🔲 Planned | P2 |

                                                                            ---

                                                                            ## 🎨 Content Specifications

                                                                            ### Video Format
                                                                            - **Duration:** 60 seconds maximum
                                                                            - - **Aspect Ratio:** 9:16 (vertical)
                                                                              - - **Resolution:** 1080x1920 (Full HD)
                                                                                - - **Frame Rate:** 30fps
                                                                                 
                                                                                  - ### Style Guidelines
                                                                                  - - **Aesthetic:** Cyberpunk, Neon, Futuristic
                                                                                    - - **Color Palette:** Deep blues, purples, neon pinks, electric greens
                                                                                      - - **Typography:** Tech/futuristic fonts
                                                                                        - - **Transitions:** Glitch effects, digital distortion
                                                                                         
                                                                                          - ### Audio Specifications
                                                                                          - - **Narration:** AI-generated voice, mysterious/tech tone
                                                                                            - - **Background Music:** Synthwave, ambient electronic
                                                                                              - - **Audio Levels:** Voice -6dB, Music -18dB
                                                                                               
                                                                                                - ---

                                                                                                ## 🔐 Security Considerations

                                                                                                1. **API Keys:** Stored in .env file (gitignored)
                                                                                                2. 2. **Telegram Authentication:** User ID validation
                                                                                                   3. 3. **Webhook Security:** Make.com custom webhook with unique URL
                                                                                                      4. 4. **Rate Limiting:** Implemented in bot for API protection
                                                                                                        
                                                                                                         5. ---
                                                                                                        
                                                                                                         6. ## 📊 Monitoring & Logging
                                                                                                        
                                                                                                         7. - **Bot Logging:** Python logging module (INFO level)
                                                                                                            - - **Make.com:** Built-in execution history
                                                                                                              - - **Error Handling:** Try-catch blocks with user feedback
                                                                                                               
                                                                                                                - ---
                                                                                                                
                                                                                                                ## 📝 Change Log
                                                                                                                
                                                                                                                | Version | Date | Changes |
                                                                                                                |---------|------|---------|
                                                                                                                | 0.1 | Jan 21, 2026 | Initial bot setup with Telegram integration |
                                                                                                                | 0.2 | Jan 21, 2026 | Added Gemini AI integration |
                                                                                                                | 0.3 | Jan 21, 2026 | Connected Make.com webhook |
                                                                                                                | 1.0 | Jan 22, 2026 | PRD documentation created |
                                                                                                                
                                                                                                                ---
                                                                                                                
                                                                                                                ## 👥 Contributors
                                                                                                                
                                                                                                                - **Matthieu Kokabi** - Project Owner & Developer
                                                                                                                - - **Claude (Anthropic)** - AI Assistant & Documentation
