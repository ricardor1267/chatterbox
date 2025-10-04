#!/usr/bin/env python3
"""
Local testing script for Chatterbox RunPod handler
Run this to test the handler locally before deploying
"""

import sys
import os
import json

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the handler
from handler import handler

def test_basic_english():
    """Test basic English TTS"""
    print("\n=== Testing Basic English TTS ===")
    job = {
        "input": {
            "text": "Hello, this is a test of the Chatterbox English text to speech system.",
            "model_type": "english",
            "exaggeration": 0.5,
            "cfg_weight": 0.5
        }
    }
    
    result = handler(job)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return False
    else:
        print(f"✅ Success!")
        print(f"   Duration: {result['duration']}s")
        print(f"   Sample Rate: {result['sample_rate']}Hz")
        print(f"   Model: {result['model_used']}")
        return True


def test_multilingual():
    """Test multilingual TTS with different languages"""
    languages = [
        ("en", "Hello, this is English text to speech."),
        ("es", "Hola, este es un sistema de síntesis de voz en español."),
        ("fr", "Bonjour, ceci est un système de synthèse vocale en français."),
    ]
    
    print("\n=== Testing Multilingual TTS ===")
    
    all_passed = True
    for lang_id, text in languages:
        print(f"\nTesting {lang_id}...")
        job = {
            "input": {
                "text": text,
                "model_type": "multilingual",
                "language_id": lang_id,
                "exaggeration": 0.5,
                "cfg_weight": 0.5
            }
        }
        
        result = handler(job)
        
        if "error" in result:
            print(f"   ❌ Error: {result['error']}")
            all_passed = False
        else:
            print(f"   ✅ Success!")
            print(f"      Duration: {result['duration']}s")
            print(f"      Language: {result['language']}")
    
    return all_passed


def test_error_handling():
    """Test error handling"""
    print("\n=== Testing Error Handling ===")
    
    # Test missing text
    print("\nTesting missing text...")
    job = {"input": {"model_type": "english"}}
    result = handler(job)
    
    if "error" in result:
        print(f"   ✅ Correctly caught error: {result['error']}")
    else:
        print(f"   ❌ Should have returned error")
        return False
    
    # Test invalid language
    print("\nTesting invalid language...")
    job = {
        "input": {
            "text": "Test",
            "model_type": "multilingual",
            "language_id": "invalid_lang"
        }
    }
    result = handler(job)
    
    if "error" in result:
        print(f"   ✅ Correctly caught error: {result['error']}")
    else:
        print(f"   ❌ Should have returned error")
        return False
    
    return True


def test_parameters():
    """Test various parameter combinations"""
    print("\n=== Testing Parameter Variations ===")
    
    parameter_sets = [
        {
            "name": "High exaggeration",
            "params": {"exaggeration": 1.5, "cfg_weight": 0.3}
        },
        {
            "name": "Low temperature",
            "params": {"temperature": 0.5, "cfg_weight": 0.5}
        },
        {
            "name": "Custom seed",
            "params": {"seed": 42, "exaggeration": 0.5}
        }
    ]
    
    all_passed = True
    for test_set in parameter_sets:
        print(f"\nTesting {test_set['name']}...")
        job = {
            "input": {
                "text": "This is a parameter variation test.",
                "model_type": "multilingual",
                "language_id": "en",
                **test_set['params']
            }
        }
        
        result = handler(job)
        
        if "error" in result:
            print(f"   ❌ Error: {result['error']}")
            all_passed = False
        else:
            print(f"   ✅ Success with params: {test_set['params']}")
    
    return all_passed


def main():
    """Run all tests"""
    print("=" * 60)
    print("Chatterbox RunPod Handler - Local Testing")
    print("=" * 60)
    
    tests = [
        ("Basic English TTS", test_basic_english),
        ("Multilingual TTS", test_multilingual),
        ("Error Handling", test_error_handling),
        ("Parameter Variations", test_parameters),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
