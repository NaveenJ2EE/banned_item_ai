# Banned Item Detection System

## 1. Executive Summary

This document describes a production-ready AI system for detecting banned items (starting with weapons) on the x marketplace using computer vision. The system is designed to be scalable, auditable, and compliant with marketplace governance requirements. It uses transfer learning on a lightweight vision model (MobileNetV3) and supports human-in-the-loop review for low-confidence predictions.

---

## 2. Business Problem

Marketplace compliance teams must ensure that prohibited items (e.g., guns, knives, alcohol, adult products) are not listed on the platform. Manual review alone does not scale with millions of listings.

**Goal:** Automatically detect banned items from seller-uploaded images and route uncertain cases for manual review.

---

## 3. High-Level Architecture

### 3.1 System Flow

1. Seller uploads product images
2. Image is sent to Banned Item Detection Service
3. Vision model predicts category + confidence
4. OCR extracts text (optional)
5. Decision engine applies thresholds
6. Outcome:

   * Auto-block
   * Manual review
   * Allow listing

### 3.2 Architecture Diagram (Logical)

```
[ Seller Upload ]
        |
        v
[ Image Ingestion API ]
        |
        v
[ Vision Model (MobileNetV3) ] -----> [ Confidence Score ]
        |
        v
[ OCR Module (EasyOCR) ]
        |
        v
[ Policy & Threshold Engine ]
        |
        +--> Auto Block
        +--> Manual Review Queue
        +--> Allow Listing
```

---

## 4. Model Architecture

### 4.1 Model Choice

* **Model:** MobileNetV3 (Large)
* **Why:**

  * Lightweight and fast
  * Suitable for high-throughput inference
  * Proven performance on object classification tasks

### 4.2 Training Strategy

* Pretrained on ImageNet (1.2M images, 1000 classes)
* Fine-tuned on Flipkart-style compliance data
* Current scope: Binary classification (gun vs not_gun)

### 4.3 Transfer Learning

* Backbone layers frozen initially
* Custom classifier head added
* Supports progressive unfreezing for higher accuracy

---

## 5. Dataset Strategy

### 5.1 Folder Structure

```
data/
 ├── train/
 │    ├── gun/
 │    └── not_gun/
 ├── val/
 │    ├── gun/
 │    └── not_gun/
 └── test/
      ├── gun/
      └── not_gun/
```

### 5.2 Data Principles

* Negative samples (allowed items) > banned items
* Diverse angles, lighting, and backgrounds
* No explicit or unsafe content in POC data

---

## 6. Evaluation Metrics

Compliance systems prioritize **recall** over pure accuracy.

Tracked metrics:

* Precision
* Recall (critical for banned items)
* F1-score
* Confidence distribution

Target (production):

* Gun recall > 95%
* False negatives minimized

---

## 7. Decision Logic

| Confidence Score | Action        |
| ---------------- | ------------- |
| >= 0.85          | Auto Block    |
| 0.60 – 0.85      | Manual Review |
| < 0.60           | Allow         |

This ensures safety while controlling false positives.

---

## 8. Scalability & Production Readiness

### 8.1 Scaling Training

* GPU-based training on cloud
* Batch loading with PyTorch DataLoader
* Dataset stored on object storage (S3/GCS)

### 8.2 Scaling Inference

* FastAPI-based microservice
* Horizontal scaling via Kubernetes
* Model versioning and rollback supported

---

## 9. Governance & Compliance

* Clear audit trail for training data
* Model version tagging
* Human-in-the-loop review
* No automated enforcement without confidence thresholds

---

## 10. Future Enhancements

* Multi-class classification (gun, knife, alcohol, adult)
* Ensemble vision models
* LLM-based policy reasoning (optional)
* Active learning from review feedback

---

# README

## Project: Banned Item AI Detection

### Overview

This project detects banned items from product images using a deep learning vision model. It is designed as a foundation for marketplace compliance systems.

### Tech Stack

* Python 3.12
* PyTorch
* TorchVision
* OpenCV
* EasyOCR
* FastAPI (optional deployment)

### Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Training

```bash
python src/train.py
```

### Inference Test

```bash
python test_model.py
```

### Output

```
('gun', 0.82, 'optional ocr text')
```

### Notes

* This repository is for POC and internal evaluation
* Production training must use policy-approved datasets

---

## Maintainer Notes

This project follows industry-standard ML practices used in large marketplaces such as Flipkart and Amazon.
