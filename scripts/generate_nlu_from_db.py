#!/usr/bin/env python3
import pandas as pd
import yaml
import random
from pathlib import Path

def generate_variations(question):
    """Generate variations of a question with typos and synonyms."""
    variations = [question.lower()]
    
    # Common word replacements
    replacements = {
        'how': ['hw', 'hwo'],
        'what': ['wat', 'wht'],
        'where': ['wher', 'were'],
        'when': ['wen', 'whn'],
        'can': ['cn', 'cna'],
        'admission': ['admision', 'addmission'],
        'fees': ['fee', 'fess'],
        'hostel': ['hostl', 'hostle'],
        'placement': ['placment', 'placements'],
        'scholarship': ['scholership', 'scholarshp'],
        'eligibility': ['eligibilty', 'eligiblity'],
        'university': ['univrsity', 'universty'],
        'course': ['cours', 'corse'],
        'pdeu': ['pdu', 'pde']
    }
    
    words = question.lower().split()
    for i, word in enumerate(words):
        if word in replacements:
            for replacement in replacements[word]:
                new_words = words.copy()
                new_words[i] = replacement
                variations.append(' '.join(new_words))
    
    # Add shortened versions
    if len(words) > 3:
        variations.append(' '.join(words[:3]))
    
    return variations[:5]  # Limit to 5 variations per question

def main():
    # Load the questions database
    db_path = Path(__file__).parent.parent / 'data' / 'questions_db.csv'
    try:
        df = pd.read_csv(db_path, quotechar='"', escapechar='\\')
    except:
        # Fallback: create basic intents if CSV parsing fails
        df = pd.DataFrame({
            'question': [
                'How do I apply for admission?', 'What is the fee structure?', 'Tell me about hostel facilities',
                'What about placements?', 'Which courses are available?', 'What is the eligibility criteria?'
            ],
            'intent': ['admission_process', 'fees', 'hostel', 'placement', 'courses', 'eligibility']
        })
    
    # Group questions by intent
    intent_groups = df.groupby('intent')
    
    nlu_data = {
        'version': '3.1',
        'nlu': []
    }
    
    # Generate NLU examples for each intent
    for intent_name, group in intent_groups:
        examples = []
        
        for _, row in group.iterrows():
            question = row['question']
            variations = generate_variations(question)
            examples.extend(variations)
        
        # Add some generic examples for common intents
        if intent_name == 'greet':
            examples.extend(['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'namaste', 'hii', 'helo'])
        elif intent_name == 'goodbye':
            examples.extend(['bye', 'goodbye', 'see you', 'thanks', 'thank you', 'thnks', 'by'])
        elif intent_name == 'affirm':
            examples.extend(['yes', 'yeah', 'yep', 'correct', 'right', 'ok', 'okay', 'sure'])
        elif intent_name == 'deny':
            examples.extend(['no', 'nope', 'not really', 'wrong', 'incorrect', 'nah'])
        
        # Remove duplicates and limit examples
        examples = list(set(examples))[:50]  # Limit to 50 examples per intent
        
        if examples:
            nlu_data['nlu'].append({
                'intent': intent_name,
                'examples': '|\n    - ' + '\n    - '.join(examples)
            })
    
    # Add lookup tables and synonyms
    nlu_data['nlu'].extend([
        {
            'lookup': 'university_names',
            'examples': '|\n    - PDEU\n    - Pandit Deendayal Energy University\n    - pdeu\n    - pdu\n    - pde'
        },
        {
            'synonym': 'PDEU',
            'examples': '|\n    - pdeu\n    - pdu\n    - pde\n    - Pandit Deendayal Energy University'
        },
        {
            'synonym': 'admission',
            'examples': '|\n    - admissions\n    - admision\n    - addmission\n    - enrollment'
        },
        {
            'synonym': 'fees',
            'examples': '|\n    - fee\n    - fess\n    - cost\n    - charges\n    - tuition'
        }
    ])
    
    # Write to NLU file
    nlu_path = Path(__file__).parent.parent / 'data' / 'nlu.yml'
    with open(nlu_path, 'w', encoding='utf-8') as f:
        yaml.dump(nlu_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"Generated NLU file with {len(nlu_data['nlu'])} intents")
    total_examples = sum(len(item.get('examples', '').split('\n')) for item in nlu_data['nlu'] if 'intent' in item)
    print(f"Total examples: {total_examples}")

if __name__ == "__main__":
    main()