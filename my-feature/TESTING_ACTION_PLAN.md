# Clarivox - Functional Testing Action Plan

**Priority**: URGENT  
**Estimated Time**: 4-6 hours  
**Required For**: Client approval

---

## 🎯 Objective

Satisfy the client's requirement:
> "I'd like confirmation that you're running **functional tests**, not just validating the code compiles. Let's make sure logs, edge case handling, error outputs, and overall behavior are all being **recorded and working as intended**—especially around the audio, transcription, and FHIR flow."

---

## 📋 Checklist

### Phase 1: Setup & Basic Execution (30 minutes)

- [ ] **1.1** Copy test audio file
  ```bash
  cd d:\clarivox\Clarivox\clarivox_clone\my-feature
  copy data\917b9e45-7b18-4099-828c-0d1bbf8faf2a.m4a tests\assets\sample_voicemail.mp3
  ```

- [ ] **1.2** Install test dependencies
  ```bash
  pip install pytest pytest-cov pytest-html httpx
  ```

- [ ] **1.3** Run existing tests
  ```bash
  pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing --html=test_report.html
  ```

- [ ] **1.4** Document initial results
  - Screenshot of test output
  - Note pass/fail for each test
  - Record coverage percentage

---

### Phase 2: Edge Case Tests (2 hours)

#### Audio Validation Edge Cases

- [ ] **2.1** Create `tests/test_audio_edge_cases.py`:
  ```python
  def test_corrupted_audio_file()
  def test_silent_audio()
  def test_audio_too_short()
  def test_audio_too_long()
  def test_oversized_file()
  def test_invalid_mime_type()
  def test_wrong_file_extension()
  ```

#### PII Sanitization Tests (CRITICAL - Currently Missing)

- [ ] **2.2** Create `tests/test_pii_sanitizer.py`:
  ```python
  def test_phone_number_redaction()
  def test_ssn_redaction()
  def test_email_redaction()
  def test_multiple_pii_patterns()
  def test_partial_phone_numbers()
  def test_international_phone_formats()
  ```

#### Intent Extraction Edge Cases

- [ ] **2.3** Add to `tests/test_intent_extractor.py`:
  ```python
  def test_ambiguous_intent()
  def test_multiple_intents_primary_selection()
  def test_no_clear_intent()
  def test_crisis_false_positives()
  def test_crisis_subtle_detection()
  ```

---

### Phase 3: Functional Validation (1.5 hours)

#### Logging Validation

- [ ] **3.1** Create `tests/test_logging_validation.py`:
  ```python
  def test_trace_id_propagation()
  def test_all_stages_logged()
  def test_error_logging_format()
  def test_metrics_logging()
  def test_log_file_creation()
  ```

#### Error Output Validation

- [ ] **3.2** Create `tests/test_error_outputs.py`:
  ```python
  def test_audio_validation_error_response()
  def test_transcription_error_response()
  def test_intent_extraction_error_response()
  def test_fhir_generation_error_response()
  def test_error_response_structure()
  def test_error_status_codes()
  ```

#### End-to-End Flow

- [ ] **3.3** Enhance `tests/test_audio_pipeline.py`:
  ```python
  def test_full_pipeline_medication_refill()
  def test_full_pipeline_crisis_detection()
  def test_full_pipeline_multiple_symptoms()
  def test_background_task_cleanup()
  def test_metrics_collection()
  ```

---

### Phase 4: Documentation (1 hour)

- [ ] **4.1** Create `TEST_RESULTS.md`:
  ```markdown
  # Test Execution Report
  - Date/Time of execution
  - Environment details
  - All test results (pass/fail)
  - Coverage metrics
  - Failed tests explanations
  - Screenshots
  ```

- [ ] **4.2** Create `FUNCTIONAL_TEST_EVIDENCE.md`:
  ```markdown
  # Evidence of Functional Testing
  
  ## Logs Validation
  - Screenshot of logs with trace IDs
  - Example log entries for each stage
  
  ## Edge Case Handling
  - List of edge cases tested
  - Test results for each
  
  ## Error Outputs
  - Example error responses
  - Validation of error structure
  
  ## Audio → FHIR Flow
  - Input: Audio file details
  - Output: Transcription
  - Output: Intent extraction
  - Output: FHIR bundle
  - Proof of end-to-end functionality
  ```

- [ ] **4.3** Record test execution video (optional but recommended):
  - Show tests running
  - Show coverage report
  - Show logs being generated
  - Show error handling in action

---

### Phase 5: Final Verification (30 minutes)

- [ ] **5.1** Run complete test suite:
  ```bash
  pytest tests/ -v --cov=app --cov-report=html --html=final_test_report.html
  ```

- [ ] **5.2** Verify minimum coverage targets:
  - Overall: >75%
  - Critical modules (audio_validator, pii_sanitizer, intent_extractor): >85%

- [ ] **5.3** Manual functional test:
  ```bash
  # Start server
  uvicorn app.main:app --reload
  
  # Upload test audio via /docs
  # Verify response
  # Check logs/trace.log
  # Verify FHIR output
  ```

- [ ] **5.4** Create final deliverable package:
  ```
  DELIVERABLE/
  ├── TEST_RESULTS.md
  ├── FUNCTIONAL_TEST_EVIDENCE.md
  ├── test_report.html
  ├── htmlcov/ (coverage report)
  ├── sample_logs.txt
  └── test_execution_video.mp4 (optional)
  ```

---

## 🎬 Quick Start Script

Save this as `run_functional_tests.sh`:

```bash
#!/bin/bash

echo "=== Clarivox Functional Testing ==="
echo ""

# Setup
echo "1. Setting up test audio..."
cp data/917b9e45-7b18-4099-828c-0d1bbf8faf2a.m4a tests/assets/sample_voicemail.mp3

# Install dependencies
echo "2. Installing test dependencies..."
pip install -q pytest pytest-cov pytest-html httpx

# Run tests
echo "3. Running functional tests..."
pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing --html=test_report.html

# Display results
echo ""
echo "=== Test Execution Complete ==="
echo "📊 Coverage report: htmlcov/index.html"
echo "📋 Test report: test_report.html"
echo ""

# Check logs
echo "4. Checking logs..."
if [ -f "logs/trace.log" ]; then
    echo "✅ Logs generated successfully"
    echo "Last 10 log entries:"
    tail -n 10 logs/trace.log
else
    echo "❌ No logs found"
fi

echo ""
echo "=== Next Steps ==="
echo "1. Review test_report.html"
echo "2. Review coverage report in htmlcov/"
echo "3. Check logs/trace.log for trace IDs"
echo "4. Document results in TEST_RESULTS.md"
```

---

## 📊 Success Criteria

Before showing to client, verify:

✅ **All tests pass** (or failures are documented with fixes)  
✅ **Coverage >75%**  
✅ **E2E audio pipeline test executed successfully**  
✅ **Logs captured with trace IDs**  
✅ **Edge cases tested and documented**  
✅ **Error outputs validated**  
✅ **PII sanitization tested** (HIPAA compliance)  
✅ **Test execution report created**  
✅ **Evidence documented**

---

## 🚨 Blockers & Mitigations

| Potential Blocker | Mitigation |
|-------------------|------------|
| Whisper model not downloaded | Pre-download: `whisper --model base --download-only` |
| Missing dependencies | Run: `pip install -r requirements.txt` fully |
| Test audio file issues | Use provided `917b9e45-7b18-4099-828c-0d1bbf8faf2a.m4a` |
| spaCy model missing | Run: `python -m spacy download en_core_web_sm` |
| FFmpeg not installed | Install FFmpeg system-wide |

---

## 📞 Client Communication Template

After completing testing, send:

```
Subject: Clarivox Functional Testing - Complete

Hi [Client],

I've completed comprehensive functional testing of the Clarivox MVP, addressing all your requirements:

✅ Functional tests executed (not just compilation checks)
✅ Logs validated - trace IDs working across all stages
✅ Edge case handling tested (15+ edge cases)
✅ Error outputs validated - proper structure confirmed
✅ End-to-end audio → transcription → FHIR flow verified

Test Results:
- Total Tests: [X]
- Passed: [X]
- Coverage: [X]%
- Documentation: See attached TEST_RESULTS.md

Evidence provided:
- Test execution report (test_report.html)
- Coverage report (htmlcov/)
- Sample logs with trace IDs
- Edge case test results
- Error handling demonstrations

The system has been validated for:
- Audio processing with various formats
- PII sanitization (HIPAA compliant)
- Intent extraction accuracy
- FHIR resource generation
- Crisis detection
- Error handling

Please review the attached documentation. Happy to walk through any specific test cases.

Best regards,
[Your Name]
```

---

## 🎯 Time Estimate by Phase

| Phase | Time | Can Parallelize? |
|-------|------|------------------|
| Phase 1: Setup | 30 min | No |
| Phase 2: Edge Cases | 2 hours | Yes (split by module) |
| Phase 3: Functional | 1.5 hours | Partially |
| Phase 4: Documentation | 1 hour | No |
| Phase 5: Verification | 30 min | No |
| **TOTAL** | **5.5 hours** | |

**With 2 people**: ~3.5 hours  
**With full team focus**: Can complete in 1 day

---

## ✅ Definition of Done

- [ ] Client can run tests and see them pass
- [ ] Client can see coverage report showing >75%
- [ ] Client can see logs with trace IDs for a real request
- [ ] Client can see edge cases being handled
- [ ] Client can see proper error responses
- [ ] Client can see full audio → FHIR pipeline working
- [ ] All requirements from client's message satisfied
- [ ] Documentation explains what was tested and results

**When all boxes checked → Ready for client review** 🎉
