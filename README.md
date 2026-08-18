<div align="center">

# Surgical Tool Detection & Tracking

**YOLOv8 + ByteTrack for detecting and tracking surgical instruments in laparoscopic video**

![YOLOv8](https://img.shields.io/badge/Model-YOLOv8n-blue?style=flat-square)
![ByteTrack](https://img.shields.io/badge/Tracking-ByteTrack-purple?style=flat-square)
![CholecTrack20](https://img.shields.io/badge/Dataset-CholecTrack20-orange?style=flat-square)

</div>

---

## Overview

This project looks at how well a surgical tool detector works when the video gets messy.

I trained YOLOv8n on [CholecTrack20](https://github.com/CAMMA-public/cholectrack20), a dataset of laparoscopic cholecystectomy videos with annotations for seven surgical tool classes. I then compared performance on normal frames with frames containing **bleeding, smoke, or occlusion**.

I also used ByteTrack to track detected tools across video frames.

---

## Results

|              | Clean mAP50 | Hard-Condition mAP50 |   Drop  |
| :----------- | :---------: | :------------------: | :-----: |
| **Overall**  |  **0.622**  |       **0.370**      | **40%** |
| Grasper      |    0.726    |         0.376        |   48%   |
| Specimen-bag |    0.888    |         0.480        |   46%   |
| Hook         |    0.872    |         0.513        |   41%   |

Performance dropped noticeably when the model was evaluated on frames with bleeding, smoke, or occlusion.

Bipolar, scissors, irrigator, and clipper are not included in the table because there were too few clean validation examples to make a fair comparison.

### Evaluation Plots

* [`training_metrics.png`](results/training_metrics.png)
* [`confusion_matrix.png`](results/confusion_matrix.png)
* [`BoxPR_curve.png`](results/BoxPR_curve.png)

---

## Demo

**[Watch the full specimen-bag tracking demo](demos/vid01_clip4_specimenbag.mp4)**

A few other examples are in [`demos/`](demos/), including hooks, graspers, irrigator, and a clipper-to-scissors tool switch.

---

## Irrigator Analysis

The irrigator was the weakest class, with an mAP50 of approximately **0.03**.

I wanted to check whether the problem was mainly caused by the tool being small in the image, so I trained another model at **640px instead of 416px**. The higher resolution did not make a meaningful difference.

Looking at the training data gave another possible explanation:

| Class     | Training Instances |
| :-------- | :----------------: |
| Grasper   |       15,811       |
| Irrigator |         663        |

There were about **25× more grasper instances than irrigator instances**.

I also ran a low-confidence analysis on frames containing irrigators ([`irrigator_diagnosis.png`](results/irrigator_diagnosis.png)). The model generally was not confidently predicting another tool class. Its predictions were simply very weak, with the strongest predictions around **16.5% confidence**.

Based on these tests, class imbalance seems like a more likely issue than image resolution.

---


### Script Breakdown

<details>
<summary><b>View script descriptions</b></summary>

| Script                                           | Purpose                                           |
| :----------------------------------------------- | :------------------------------------------------ |
| `download_cholectrack20.py`                      | Downloads CholecTrack20 through Synapse           |
| `build_yolo_from_cholectrack.py`                 | Converts CholecTrack20 annotations to YOLO format |
| `train_v2.py` / `train_v3.py`                    | Training at 416px and 640px                       |
| `check_class_balance.py`                         | Checks class distribution                         |
| `check_box_sizes.py`                             | Analyzes bounding-box sizes                       |
| `diagnose_irrigator.py`                          | Investigates irrigator predictions                |
| `build_occlusion_split.py`                       | Builds clean and hard-condition validation sets   |
| `evaluate_occlusion.py`                          | Evaluates detection by condition                  |
| `build_tracking_demo.py` / `build_more_demos.py` | Generates detection and ByteTrack demos           |

</details>

---

## Approach

**Detection:** YOLOv8n from Ultralytics

**Tracking:** ByteTrack through Ultralytics' `.track()` interface

**Training:** 416px and 640px image sizes, trained CPU-only

**Dataset:** CholecTrack20 with its official video-level train/validation/test split

**Condition analysis:** Used CholecTrack20's existing bleeding, smoke, and occluded labels

The final 640px training run took about **37 hours on CPU**.

---

## Limitations

* Tracking has only been evaluated qualitatively through the demo videos
* The detector was trained CPU-only
* Several classes have relatively few training examples
* The system has not been tested on live surgical video
* Results are based on CholecTrack20 and may not generalize to other surgical datasets or operating environments

---

## Dataset & Citation

This project uses **CholecTrack20: A Multi-Perspective Tracking Dataset for Surgical Tools** by Chinedu Innocent Nwoye, Kareem Elgohary, Anvita Srinivas, Fauzan Zaid, Joël L. Lavanchy, and Nicolas Padoy.

[CholecTrack20 GitHub repository](https://github.com/CAMMA-public/cholectrack20)

The dataset is released under **CC BY-NC-SA 4.0** and is subject to the authors' Data Use Agreement. The original dataset and annotations are not included in this repository.

If you use the dataset, please cite:

```bibtex
@InProceedings{nwoye2023cholectrack20,
  author    = {Nwoye, Chinedu Innocent and Elgohary, Kareem and Srinivas, Anvita and Zaid, Fauzan and Lavanchy, Joël L. and Padoy, Nicolas},
  title     = {CholecTrack20: A Multi-Perspective Tracking Dataset for Surgical Tools},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2025}
}
```

---

## About

Built independently during **Summer 2026** as a computer vision project exploring the intersection of medical robotics and surgical systems.
