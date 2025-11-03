# PDEU CampusGuide - Production-Ready Chatbot

A comprehensive, context-aware chatbot for Pandit Deendayal Energy University (PDEU) admissions and campus information.

## 🚀 Features

### ✨ Core Capabilities
- **Context Awareness**: Multi-turn conversations with slot filling and state tracking
- **Spell Correction**: Handles typos and misspellings automatically
- **Large Knowledge Base**: 500+ FAQ entries covering all university aspects
- **Smart Fallback**: Intelligent fallback with suggestions when queries aren't understood
- **Form Handling**: Structured data collection for admissions and fee inquiries

### 🎯 Covered Topics
- Admission Process & Requirements
- Fee Structure & Scholarships
- Hostel Facilities & Accommodation
- Placement Statistics & Companies
- Course Details & Eligibility
- Campus Facilities & Safety
- Academic Information & Policies
- Student Life & Activities

## 📁 Project Structure

```
├── components/
│   └── spell_checker.py          # Custom spell correction component
├── data/
│   ├── nlu.yml                   # NLU training data (1000+ examples)
│   ├── stories.yml               # Conversation flows
│   ├── rules.yml                 # Business rules
│   └── questions_db.csv          # FAQ database (500+ entries)
├── actions/
│   └── actions.py                # Custom actions & form validation
├── scripts/
│   └── generate_nlu_from_db.py   # NLU generation script
├── tests/
│   └── test_stories.yml          # Test scenarios
├── final/
│   └── console_summary.txt       # Validation results
├── ui/
│   └── index.html                # Web interface
├── config.yml                    # Pipeline configuration
├── domain.yml                    # Domain definition
├── credentials.yml               # Channel credentials
└── endpoints.yml                 # Action server endpoints
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Rasa 3.x
- Required packages: pandas, rapidfuzz, pyyaml

### Installation

1. **Clone and Navigate**
   ```bash
   cd /path/to/chatbot/directory
   ```

2. **Install Dependencies**
   ```bash
   pip install rasa pandas rapidfuzz pyyaml
   ```

3. **Validate Data**
   ```bash
   rasa data validate
   ```

4. **Train the Model**
   ```bash
   rasa train
   ```

## 🚀 Running the Chatbot

### Method 1: Command Line Interface
```bash
rasa shell
```

### Method 2: Full Deployment
1. **Start Action Server** (Terminal 1)
   ```bash
   rasa run actions
   ```

2. **Start Rasa Server** (Terminal 2)
   ```bash
   rasa run --enable-api --cors "*"
   ```

3. **Open Web Interface**
   - Open `ui/index.html` in your browser
   - Or access via `http://localhost:5005`

### Method 3: Interactive Learning
```bash
rasa interactive
```

## 🧪 Testing

### Run All Tests
```bash
rasa test
```

### Test Specific Components
```bash
# Test NLU only
rasa test nlu

# Test Core only  
rasa test core

# Test Stories
rasa test core --stories tests/test_stories.yml
```

### Manual Testing Examples
Try these inputs to test spell correction and context awareness:

```
User: "helo, hw can I apply for admision?"
User: "wat is the fess structure for btech?"
User: "tell me about hostl facilities"
User: "placment statistics and companies"
```

## 📊 Database Management

### Updating the FAQ Database

1. **Edit the Database**
   - Modify `data/questions_db.csv`
   - Add new questions, answers, categories, and intents
   - Maintain CSV format: `question,answer,category,intent`

2. **Regenerate NLU Data**
   ```bash
   python scripts/generate_nlu_from_db.py
   ```

3. **Retrain the Model**
   ```bash
   rasa train
   ```

### Adding New Intents

1. **Update Domain** (`domain.yml`)
   - Add new intent to `intents` section
   - Add corresponding response in `responses` section

2. **Update NLU** (`data/nlu.yml`)
   - Add training examples for new intent
   - Include variations and typos

3. **Update Stories/Rules**
   - Add conversation flows in `data/stories.yml`
   - Add business rules in `data/rules.yml`

## 🔧 Configuration

### Pipeline Components (config.yml)
1. **SpellChecker** - Corrects typos early in pipeline
2. **WhitespaceTokenizer** - Tokenizes input text
3. **RegexFeaturizer** - Extracts regex features
4. **LexicalSyntacticFeaturizer** - Linguistic features
5. **CountVectorsFeaturizer** - Bag of words features
6. **DIETClassifier** - Intent classification & entity extraction
7. **EntitySynonymMapper** - Maps entity synonyms
8. **ResponseSelector** - Selects appropriate responses
9. **FallbackClassifier** - Handles low-confidence predictions

### Key Policies
- **MemoizationPolicy** - Remembers exact conversation patterns
- **RulePolicy** - Enforces business rules
- **TEDPolicy** - Transformer-based dialogue management

## 🎛️ Customization

### Adding New Spell Corrections
Edit `components/spell_checker.py`:
```python
self.corrections = {
    'new_word': ['typo1', 'typo2', 'variation'],
    # Add more corrections
}
```

### Modifying Responses
Edit `domain.yml` responses section:
```yaml
responses:
  utter_new_response:
    - text: "Your custom response here"
      buttons:
        - title: "Button Text"
          payload: "/intent_name"
```

### Adding Custom Actions
1. Create new action in `actions/actions.py`
2. Add action to `domain.yml` actions section
3. Use in stories/rules

## 📈 Performance Optimization

### Training Optimization
- **Increase epochs** for better accuracy (config.yml)
- **Add more training examples** for low-performing intents
- **Use data augmentation** for better generalization

### Response Time Optimization
- **Cache FAQ responses** in actions
- **Optimize database queries** 
- **Use async operations** where possible

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install --upgrade rasa pandas rapidfuzz
   ```

2. **Validation Errors**
   ```bash
   rasa data validate --debug
   ```

3. **Action Server Connection**
   - Ensure action server is running on port 5055
   - Check `endpoints.yml` configuration

4. **Spell Checker Not Working**
   - Verify component is first in pipeline
   - Check component import path

### Debug Mode
```bash
rasa shell --debug
rasa run --debug
```

## 📝 Maintenance

### Regular Tasks
1. **Update FAQ Database** - Add new questions monthly
2. **Review Conversations** - Analyze user interactions
3. **Retrain Model** - Incorporate new data
4. **Test Performance** - Run automated tests
5. **Monitor Metrics** - Track accuracy and response times

### Version Control
- Commit changes to training data
- Tag model versions
- Maintain changelog

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For technical support or questions:
- Create an issue in the repository
- Contact the development team
- Check Rasa documentation: https://rasa.com/docs/

## 🎯 Future Enhancements

- [ ] Multi-language support
- [ ] Voice interface integration
- [ ] Advanced analytics dashboard
- [ ] Integration with university systems
- [ ] Mobile app deployment
- [ ] Advanced NLP features

---

**Ready for Production Deployment! 🚀**

Train the model with `rasa train` and deploy with `rasa run` + `rasa run actions`.