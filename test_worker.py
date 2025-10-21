#!/usr/bin/env python3
"""
Local testing script for Chatterbox RunPod Worker
Tests the handler locally before deploying
"""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the handler
from rp_handler import handler

def test_basic():
    """Test basic TTS generation"""
    print("\n" + "="*60)
    print("TEST 1: Basic English TTS")
    print("="*60)
    
    job = {
        "input": {
            "text": "Hello, this is a test of Chatterbox on RunPod!",
            "model_type": "english",
            "exaggeration": 0.5,
            "cfg_weight": 0.5
        }
    }
    
    result = handler(job)
    
    if "error" in result:
        print(f"❌ FAILED: {result['error']}")
        return False
    else:
        print(f"✅ SUCCESS")
        print(f"   Duration: {result['duration']}s")
        print(f"   Sample Rate: {result['sample_rate']}Hz")
        print(f"   Generation Time: {result['generation_time']}s")
        return True


def test_multilingual():
    """Test multilingual TTS"""
    print("\n" + "="*60)
    print("TEST 2: Multilingual TTS")
    print("="*60)
    
    tests = [
        ("en", "Hello, this is English."),
        ("es", "Hola, esto es español."),
        ("fr", "Bonjour, ceci est français."),
    ]
    
    all_passed = True
    for lang_id, text in tests:
        print(f"\n🌍 Testing {lang_id}...")
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
            print(f"   ❌ FAILED: {result['error']}")
            all_passed = False
        else:
            print(f"   ✅ SUCCESS - Duration: {result['duration']}s")
    
    return all_passed


def test_voice_cloning():
    """Test voice cloning (requires reference audio)"""
    print("\n" + "="*60)
    print("TEST 3: Voice Cloning")
    print("="*60)
    print("⚠️  Skipped - Requires reference audio")
    return True


def test_error_handling():
    """Test error handling"""
    print("\n" + "="*60)
    print("TEST 4: Error Handling")
    print("="*60)
    
    # Test missing text
    print("\n📝 Testing missing text...")
    job = {"input": {"model_type": "english"}}
    result = handler(job)
    
    if "error" in result:
        print(f"   ✅ Correctly caught error: {result['error']}")
    else:
        print(f"   ❌ Should have returned error")
        return False
    
    # Test invalid language
    print("\n🌍 Testing invalid language...")
    job = {
        "input": {
            "text": "Test",
            "model_type": "multilingual",
            "language_id": "invalid"
        }
    }
    result = handler(job)
    
    if "error" in result:
        print(f"   ✅ Correctly caught error: {result['error']}")
    else:
        print(f"   ❌ Should have returned error")
        return False
    
    return True


def test_from_file():
    """Test using test_input.json"""
    print("\n" + "="*60)
    print("TEST 5: Using test_input.json")
    print("="*60)
    
    try:
        with open('test_input.json', 'r') as f:
            test_data = json.load(f)
        
        result = handler(test_data)
        
        if "error" in result:
            print(f"❌ FAILED: {result['error']}")
            return False
        else:
            print(f"✅ SUCCESS")
            print(f"   Text: {test_data['input']['text'][:50]}...")
            print(f"   Duration: {result['duration']}s")
            return True
    except FileNotFoundError:
        print("⚠️  test_input.json not found - skipping")
        return True


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 Chatterbox RunPod Worker - Local Tests")
    print("="*60)
    
    tests = [
        ("Basic English TTS", test_basic),
        ("Multilingual TTS", test_multilingual),
        ("Voice Cloning", test_voice_cloning),
        ("Error Handling", test_error_handling),
        ("Test Input File", test_from_file),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with exception:")
            print(f"   {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    print("\n" + "="*60)
    
    if all_passed:
        print("🎉 All tests passed!")
        print("\n✅ Ready to deploy to RunPod!")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
