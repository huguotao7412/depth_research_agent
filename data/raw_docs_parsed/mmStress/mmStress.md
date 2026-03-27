<header>PDF Download
3610926.pdf 20January 2026Total Citations:20Total Downloads:1186 ACM DIGITAL 电 Computing Machinery Associatien fer LIBRARY acmopen> CK10 Published:27September 2023</header>


CK10


ACM DIGITAL 电 Computing Machinery Associatien fer LIBRARY acmopen>


Latest updates:


RESEARCH-ARTICLE


# mmStress:Distilling Human Stress from Daily Activities via Contactless Millimeter-wave Sensing


KUN LIANG,Beijing University of Posts and Telecommunications,Beijing,Beijing,China ANFU ZHOU,Beijing University of Posts and Telecommunications,Beijing,Beijing,China ZHAN ZHANG,Beijing University of Posts and Telecommunications,Beijing,Beijing,China HAO ZHOU,Beijing University of Posts and Telecommunications,Beijing,Beijing,China HUADONG MA,Beijing University of Posts and Telecommunications,Beijing,Beijing,China CHENSHU WU,The University of Hong Kong,Hong Kong,Hong Kong


Open Access Support provided by:The University of Hong Kong Beijing University of Posts and Telecommunications


PDF Download
3610926.pdf 20January 2026Total Citations:20Total Downloads:1186


Published:27September 2023


Citation in BibTeX format


Proceedings of the ACM on Interactive,Mobile,Wearable and Ubiquitous Technologies,Volume 7,Issue 3(September 2023)h ps://doi.org/10.1145/3610926EISSN:2474-9567


<footer>Proceedings of the ACM on Interactive,Mobile,Wearable and Ubiquitous Technologies,Volume 7,Issue 3(September 2023)h ps://doi.org/10.1145/3610926EISSN:2474-9567</footer>
<header>110</header>


# mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing


KUN LIANG,Beijing University of Posts and Telecommunications,China ANFU ZHOU,Beijing University of Posts and Telecommunications,China ZHAN ZHANG,Beijing University of Posts and Telecommunications,China HAO ZHOU,Beijing University of Posts and Telecommunications,China HUADONG MA,Beijing University of Posts and Telecommunications,China CHENSHU WU,University of Hong Kong,China


Long-term exposure to stress hurts human's mental and even physical health,and stress monitoring is of increasing significance in the prevention,diagnosis,and management of mental illness and chronic disease.However,current stress monitoring methods are either burdensome or intrusive,which hinders their widespread usage in practice.In this paper,we propose mmStress,a contact-less and non-intrusive solution,which adopts a millimeter-wave radar to sense a subject's activities of daily living,from which it distills human stress.mmStress is built upon the psychologically-validated relationship between human stress and "displacement activities",i.e.,subjects under stress unconsciously perform fidgeting behaviors like scratching,wandering around,tapping foot,etc.Despite the conceptual simplicity,to realize mmStress,the key challenge lies in how to identify and quantify the latent displacement activities autonomously,as they are usually transitory and submerged in normal daily activities,and also exhibit high variation across different subjects.To address these challenges,we custom-design a neural network that learns human activities from both macro and micro timescales and exploits the continuity of human activities to extract features of abnormal displacement activities accurately.Moreover,we also address the unbalance stress distribution issue by incorporating a post-hoc logit adjustment procedure during model training.We prototype,deploy and evaluate mmStress in ten volunteers'apartments for over four weeks,and the results show that mmStress achieves a promising accuracy of ∽80%in classifying low,medium and high stress.In particular,mmStress manifests advantages,particularly under free human movement scenarios,which advances the state-of-the-art that focuses on stress monitoring in quasi-static


CCS Concepts:•Human-centered computing →Ubiquitous and mobile computing design and evaluation


Additional Key Words and Phrases:Human Stress Monitoring,Human Activities Sensing,Contact-less Sensing,mmWave Radar


# ACM Reference Format:


Kun Liang,Anfu Zhou,Zhan Zhang,Hao Zhou,Huadong Ma,and Chenshu Wu.2023.mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing.Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.7,3,Article 110(September 2023),36


Authors'addresses:Kun Liang,shadowam@bupt.edu.cn,Beijing University of Posts and Telecommunications,Beijing,China;Anfu Zhou,zhouanfu@bupt.edu.cn,Beijing University of Posts and Telecommunications,Beijing,China;Zhan Zhang,2021010208zz@bupt.edu.cn,Beijing University of Posts and Telecommunications,Beijing,China;Hao Zhou,2022140850zhouhao@bupt.edu.cn,Beijing University of Posts and Telecommunications,Beijing,China;Huadong Ma,mhd@bupt.edu.cn,Beijing University of Posts and Telecommunications,Beijing,China;Chenshu Wu,chenshu@cs.hku.hk,University of Hong Kong,Hong Kong,


Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that
copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page.Copyrights for components of this work owned by others than the author(s)must be honored.Abstracting with credit is permitted.To copy otherwise,or republish,to post on servers or to redistribute to lists,requires prior specific permission and/or a fee.Request permissions from permissions@acm.org.
©2023Copyright held by the owner/author(s).Publication rights licensed to ACM.
2474-9567/2023/9-ART110


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


110


<footer>Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that
copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page.Copyrights for components of this work owned by others than the author(s)must be honored.Abstracting with credit is permitted.To copy otherwise,or republish,to post on servers or to redistribute to lists,requires prior specific permission and/or a fee.Request permissions from permissions@acm.org.
©2023Copyright held by the owner/author(s).Publication rights licensed to ACM.
2474-9567/2023/9-ART110 Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>110:2•Liang et al.</header>


110:2•Liang et al.




$F i g.1$.Illustration of mmStress.mmStress adopts a millimeter-wave radar to sense a subject's activities of daily living in a contact-less and non-intrusive way.Then,mmStress identifies the subject's latent stress-induced fidgeting behaviors,and quantifies his/her stress condition with the deep learning model.


# 1INTRODUCTION


Nowadays,people are under great stress,due to the accelerated pace of work and life [43].While occasional and moderate stress can be relieved by various means (e.g.,sleep,entertainment),chronic stress,i.e.,long-term exposure and accumulation of stress,hurts one's mental and even physical health [42].In particular,chronic stress is highly correlated with depression [85],anxiety [74],etc.Moreover,people with high stress are more likely to suffer from chronic diseases such as cardiovascular disease [40]and Parkinson's disease [19].Therefore,long-term stress monitoring is of great significance to gain continuous stress awareness,which can motivate one to regulate his/her stress levels and can provide physicians with data-driven insights for more personalized healthcare.


To monitor human stress,the current mainstream solution is that subjects record their stress level by filling in a well-designed questionnaire periodically,e.g.,per day.However,such an approach is obtrusive and burdensome,and users can easily lose adherence or return unreliable results [47,70].Recently,researchers employ smartphones and wearables to measure certain physiological characteristics such as galvanic skin response (GSR)[7,93],heart rate variability (HRV)[12,68],users'locations [67],or their posts on social media [77],and then to infer human stress level accordingly.However,these approaches require users to wear smart devices all the time,which is uncomfortable and hinders their widespread usage in daily life [92].


To achieve a completely non-intrusive stress monitoring solution,recent work WiStress introduces a contactless system using a millimeter-wave (mmWave)radar [26].WiStress emits mmWave signals toward a user,analyzes the signal reflected by the user to estimate heartbeats,and finally infers the user's stress,i.e.,classifying human stress into three levels of low,medium and high.While taking a pioneering step toward contactless stress monitoring,WiStress is limited to quasi-static situations only,i.e.,the target user needs to be completely still or only perform minimal activities such as flipping books and typing,at a fixed position with the chest facing the radar.This is because that WiStress relies on heartbeat motions at the scale of only a few millimeters,resulting in heartbeat signals of a smaller magnitude than some unwanted artifacts and therefore only measurable when a user is quasi-static and close to the radar.


In this paper,we move forward to break the "quasi-static"requirement and propose mmStress,a contactless system that can monitor human stress when the subject lives in an unconstrained and natural circumstance.To achieve so and overcome the drawbacks of WiStress,our system monitors stress from a subject's daily activities,instead of from heartbeats.As shown in Fig.1,mmStress places a mmWave radar at some inconspicuous point,e.g.,the ceiling corner of a room,which emits wireless signals constantly.mmStress exploits the reflected signals


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.</footer>
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:3</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:3


to recover the daily activities of the subject (e.g.,walking trajectories,posture status)and further infers stress based on the activities.It is noteworthy that mmStress is much less privacy intrusive as the mmWave radar only generates coarse-grained point cloud data of the subject (Fig.1),which describes the most active coordinates of the human body,instead of visual images generated by a camera.In addition,mmStress is insensitive to lighting conditions and can work even in the


mmStress is inspired by the psychological/medical observation that humans under stress unconsciously perform certain habitual actions (called "displacement activities"[66,90]),such as scratching,touching their faces or mouths,yawning,and wandering around.Moreover,the higher the stress level,the more frequent these actions are.Therefore,there are differences in a subject's daily activities when under different stress levels,and the basic idea of mmStress is to capture such differences ,based on which mmStress infers the subject's stress.While conceptually simple,we identify and address two main challenges when realizing


Challenge 1:Detecting the latent displacement activities.Despite the existence of displacement activities [90],they are hard to be detected due to two major reasons:(i)A displacement activity is usually transitory and submerged in other normal daily activities.For instance,a subject in acute stress may scratch his/her head from time to time,but each scratching usually lasts only a few seconds and happens irregularly in between other normal activities.(ii)Displacement activities vary widely among individuals,in terms of different fidgeting behaviors.For instance,while one subject keeps tapping his/her foot under stress,another may cross and uncross legs,etc.To meet these challenges,we design a neural network called mmStressNet,which can capture features of displacement activities.In particular,mmStressNet learns human activities at both macro and micro timescales.At the macro-scale,mmStressNet adopts a self-attention mechanism to examine the frequency,scope,and magnitude of a subject's activities,so as to identify and extract possible behavioral abnormality (i.e.,displacement activities)from all daily activities.At the micro-scale,mmStressNet uses dilated causal convolution to analyze the continuity of these activity frames using a varying time window,so as to eliminate the non-stress-related activities introduced at the preceding macro-scale stage.In this way,mmStress quantifies the latent displacement activities precisely,which in consequence leads to accurate stress


Challenge 2:Sparse mmWave sensing data and unbalanced stress distribution.In this work,we aim to make mmStress practical and train it using real-world data collected from volunteers.However,the sensed data,i.e.,the mmWave point cloud,is much more sparse than visual image [76,82],which incurs extra difficulties for behavior detection and recognition.To handle the mmWave sparsity,we up-dimensionalize the sensed data to amplify the differences across activity features,thus facilitating the feature learning of mmStressNet.In addition,we find that most of the stress data are distributed at low-stress levels.Applying conventional training approaches to such unbalanced data will favor the majority class,i.e.,the low-stress class,while confusing the minority classes (mediumto high-stress levels)with each other.To avoid this problem and improve the robustness of mmStress,we adopt the post-hoc logit adjustment procedure [63]for training.In particular,given that the distribution of the training set and test set is the same,we first derive a prior logit offset about the distribution,and then subtract this offset with the final logit of the test set.In doing so,the average precision of each stress level is


We prototype mmStress by modifying a TI IWR6843ODS mmWave radar [35].In particular,we retrofit the radar board and reduce its size to be 19cm2and equip it with a Wi-Fi module,which can be easily deployed,operates automatically and uploads sensed data (after anonymization)to a back-end cloud server for stress inference,as detailed in Sec.5.1.1.We recruit 10volunteers from various industries (schools,scientific research institutes,and enterprises)and collect daily activities for each of them for 4weeks.During the data collection,volunteers live their usual routines without any restrictions.In total,we collect 4,648,029mmWave sensing data frames,corresponding to over 1,200hours of activity data and 145,186stress values.Our evaluation using this real-world dataset leads to major findings as follows:(i)mmStress can accurately distill human activities and classify stress into three standard levels:low,medium,and high,with an average accuracy of 83.0%.(ii)mmStress manifests its advantage,particularly under free movement scenarios,with an average accuracy of 82.6%,which is


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>110:4•Liang et</header>


110:4•Liang et


complementary to the state-of-the-art WiStress that focuses on quasi-static scenarios.(iii)mmStress is robust and adaptive to new environments,with an accuracy drop by only 7.6%upon environment changes,which can be recovered through fine-tuning with a small amount of activity data in the new environment (about 10%of the original


To sum up,the contributions of mmStress are summarized as follows:


(1)We propose mmStress,a mmWave sensing system to infer human stress level,while the subject moves freely without any restriction.mmStress represents the first automatic and non-intrusive solution to exploit the psychological correlation between stress and displacement activities.
(2)We customize a neural network to detect the latent displacement activities submerged in various normal activities,and a post-hoc logit adjustment procedure to solve the stress-data unbalance problem.
(3)We prototype mmStress and perform a real-world and continuous trial study with 10volunteers over a 4-weeks duration.We build a large-scale activity-stress dataset,which will release to the public (anonymous link at https://github.com/shadowamy/Activity-Stress)to facilitate future


# 2RELATED WORK


# 2.1Stress Monitoring


Short-term stress can last from several minutes to hours,and long-term stress can last for days or even months [22,81].The negative effect of long-term stress on human health has been studied in [16,17,60,80].To monitor stress,a variety of new solutions beyond the traditional but burdensome questionnaire approach have been proposed,along with the progress of smart devices and sensing technologies,which can be categorized as


2.1.1Portable Devices Based Solutions.In recent years,the proliferation of portable devices has made it possible to monitor stress by using them to sense various physiological signals.For instance,Yoon et al.[100]place a miniaturized skin conductivity sensor at a subject's wrist to measure stress-related human galvanic skin response.Wu et al.[96]use a chest band equipped with a heartbeat sensor and acceleration sensor,and adopt machine learning algorithms to restore human stress.Such wearable devices [18,29,78]make dynamic stress monitoring possible,however,require sensors to be in contact with the human body;Unfortunately,15-35%of users refuse to wear them due to the intrusiveness [39].Therefore,researchers propose using less-intrusive smartphones for stress monitoring.For instance,Ciman et al.[15]exploit subjects'interactions with their smartphones,such as "swiping"and "scrolling"on the screen,and Ferdous et al.[23]collect statistics of the APP-usage order,so as to assess smartphone users'stress level.This approach requires users to install a specific APP and follow certain instructions,which places a burden on users.Some studies have explored smartphone localization to investigate the correlation between user location and stress,e.g.,a stressed person may visit his psychiatrist periodically.Muller's [67]and Ware's [94]teams use GPS and cellular access information to determine the location of people's visits to reflect their stress state and depression levels,respectively.These schemes are only applicable to people with a wide range of outdoor movements and are different from our work which monitors stress from activities of indoor daily


2.1.2Camera-Based Solutions.As a device-free approach,cameras at a distance can capture human images and represent a new media for stress monitoring.For instance,McDuff et al.[59]use a camera to capture changes in a person's facial expressions,and Cho et al.[13]measure human respiratory rate,and then infer human stress.However,cameras produce visual images and incur privacy concerns,and lose effect in dark,which limits their usage


2.1.3Wireless Sensing-Based Solutions.Recently,stress monitoring via wireless signals,particularly the bandwidthabundant mmWave signals,has attracted much attention.For instance,Matsui et al.[58]mount a 24GHz millimeter


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:5</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:5


wave radar on the back of a chair to measure the heart rate variability of a person,and Ha et al.[26]place a 77GHz millimeter wave radar on a table to detect the amplitude of a person's activity and extract heart rate variability,so as to measure stress level when the person is sitting still.However,the current wireless sensing systems focus on stress monitoring for static or quasi-static subjects.In contrast,mmStress aims to infer stress for subjects moving


# 2.2Wireless Sensing


2.2.1mmWave Sensing.mmWave sensing technology is rapidly emerging due to its high sensing accuracy and privacy protection advantages,and has been used in different field like cyber-physical security [48,49],industrial [25,37],autonomous driving [95]and even food/drink quality inspection [36,50].Among them,the most relevant is human sensing,from coarse-grained human movement sensing to fine-grained heartbeat sensing.To name a few,at the level of whole human torso sensing,Adib et al.[3]use a mmWave radio to track people and Li et al.[46]generate the human skeleton.Meng et al.[62]use mmWave signal for human identification,and Liu et al.[52,54]achieve more fine-grained hand gesture recognition.At the level of perceiving the subtle activities of the human body,Xu et al.[98]obtain a full-spectrum electrocardiogram of the heart by analyzing the Cardiac-mmWave scattering effect of the heart;Adhikari et al.[2]analyze the small vibrations of the surface airflow during human breathing to measure lung volume.Different from these works,mmStress infers the hidden stress conditions from the directly perceived human


2.2.2WiFi Sensing.Sensing with the Wi-Fi signal has been extensively studied in recent years,see the recent survey in [86].To name a few,at the person location level,Xie et al.[97]reduce ranging and positioning errors to sub-metre levels by stitching together the Channel State Information (CSI)measurements from multiple WiFi bands.At the level of whole human torso sensing,Tan et al.[88]use multiple WiFi links and all available WiFi channels at 5GHz to recognise human activities such as sitting and squatting,and they use CSI from WiFi devices to sense finger gestures [87].At the level of perceiving the subtle activities of the human body,Zhang et al.[69]propose the use of a Fresnel diffraction model to sense human breath.In addition,Zeng et al.[101]extend breath sensing to multiple individuals.Although WiFI is widely deployed in the home environment,a concern is that the need for multiple nodes and modifications to commercial routers may limit its practical application


# 3FEASIBILITY STUDY OF DISTILLING STRESS FROM DAILY ACTIVITIES


# 3.1Relationship Between Displacement Activities and Stress


Experiment Setup.We design an experiment not only to verify the feasibility of predicting stress by displacement activity but also to verify that mmWave can capture small actions such as head scratching and leg shaking.Finally,we verify the accuracy of the stress levels measured by the Garmin watch to show that the stress measurements from the Garmin watches are plausible as the ground truth in subsequent long-term experiments.The experiment scenario is a 2m× 2mworking cubicle with a main layout of tables,chairs and computers as shown in Fig.4.It is designed with the following procedure:


(1)Ten volunteers are recruited to induce low,medium,and high levels of stress using the Montreal Imaging
Stress Task (MIST)[20],with each level of stress induction task lasting half an hour.We use relaxing music,unprompted questions,and prompted questions (including standard basic knowledge [5],mathematical reasoning [5]and arithmetic [89])to induce low,medium and high stress,respectively.
(2)After each phase of stress induction,volunteers are asked to fill out the state scale of the State-Trait Anxiety Inventory (STAI)and report the stress level of the Visual Analogue Scale on Stress (VAS-Stress)[5].There is a 10-minute break between each phase of the stress induction task.Afterward,we use the weighted mean of the stress results from the STAI and VAS-stress questionnaires as the true stress


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>110:6•Liang et</header>


110:6•Liang et




Fig.2.The number of displacement activities produced by volunteers under each stress




Fig.3.Showcase of changes in questionnaire and watch stress scores (normalized to the same


(3)During the experiment,we use the mmWave radar and the camera to record human activity.At the end of the experiment,we use the video information captured by the camera to count the frequency of human displacement activity during each stress phase.Moreover,we compare the video data against the mmWave data,so as to detect how many displacement activities can be sensed by the mmWave


(4)In the experiment and for 3days after stress induction,we ask volunteers to wear the Garmin watch to obtain human stress levels at work and rest.In addition,the volunteers are asked to fill in the STAI and VAS-Stress questionnaires every half hour.Based on eight hours of work per person per day,we expect to collect 480questionnaires for 10users in three days.After the experiment is completed,we calculate the Pearson correlation coefficient between the questionnaire and stress readings from the


Displacement activities increases with stress.We analyze the relationship between the stress level of each volunteer's questionnaire feedback and the frequency of displacement activities through the camera data and calculate Pearson correlation coefficients,the results of which are shown in Fig.2.From the experiment result,we find that the frequency of displacement activities increases as the volunteers'stress level increases,which is consistent with the findings of previous medical studies [66,


mmWave radar captures displacement activities.In addition,we map the timestamps of the camera capturing the displacement activity to the activity data captured by the mmWave radar,so as to verify its ability to detect displacement activity.We find that,the mmWave radar can detect 88.9%of displacement activities.Moreover,mmWave radar can detect both micro and macro activities,which have significant differences over point clouds and trajectories,mainly in the following aspects:(i)The point cloud of human activity generated using mmWave describes the most active parts of the human body.When the human body has a fine-grained activity such as head scratching,the point cloud will gather in a sparse distribution and small numbers due to the small amplitude of the activity (as shown in Fig.4left),and the center of the point cloud is usually the center of that body part.(ii)When the human body has a coarse-grained activity such as walking (as shown in Fig.4right),the point cloud would be distributed in all parts of the body with a large distribution area,and the center of the point cloud is usually the thorax of the body.(iii)The trajectory moving distance over a given period is smaller for fine-grained activities than that for coarse-grained activities.Moreover,several studies clarify that the mmWaves radar can detect not only the micro-activity such as gestures [52,54]through point clouds,but also the macro-activity such as gait [62].mmStress can implicitly distinguish them due to their significant


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>mmStress: Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing • 110:7</header>


mmStress: Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing • 110:7




Fig. 4. Point cloud detected in space by mmWave while a person scratches head and walks.


Stress values from wearable and questionnaire are consistent. We verify the reliability of the Garmin watch stress
label as reference truth. Previous study [71] shows that people do not engage in strenuous activity most of the
time when they are awake. We normalize the VAS-stress score to the same scale as the STAI score and use the
mean of both as the stress score measured by the questionnaire (The scale of the questionnaire stress score is 20-80
and the watch is 0-100.). We divide the questionnaire stress scores into 3 levels (20-37, 38-44, 45-80) according
to the common STAI classification criteria [38]. This is then used as the ground truth with the watch stress
level (classification criteria in Sec. 5.4) to calculate the F1-score, which is 0.81. Moreover, the Pearson correlation
coefficient is 0.79 between the Garmin watch stress scores and the questionnaire stress scores, indicating a strong
linear correlation. Fig. 3 shows an example of stress scores submitted by one volunteer over 3 days and those
measured by the watch (normalized to the same scale), which also demonstrates a highly consistent match, as
also validated by previous studies [24, 28]. Therefore, we believe the data reported by Garmin watch is sufficient
for serving as the reference ground truth to validate and evaluate mmStress. It is also noteworthy that we are able
to gather 220 questionnaires overall, which falls significantly short of our expected total of 480. Furthermore, the
number of completed questionnaires decreases as the experiment progresses. Therefore, to monitor long-term
stress, it is highly desirable to replace such frequent and tedious questionnaire approach.


# 3.2 Findings from Long-term Deployment Experiment


Here we design a long-term experiment in which we recruit 10 additional volunteers and use mmWave radar
to collect the volunteers' activities. To acquire the ground-truth stress labels, we ask each volunteer to wear a
Garmin watch simultaneously, which can generate a stress value every 3 minutes and classify stress into low,
medium, and high levels (More details in Sec. 5). We analyze these long-term activity data, in which we take a
macroscopic view of the relationship between displacement activity collected by mmWave radar and stress: We
align these activity data with stress labels at the same period and compute 42 statistics values (or features) from
the sensed data, which can be divided into three categories: time, trajectory and point cloud. We then compute
the Pearson coefficient to quantify the correlation between each feature and the stress.


Proc. ACM Interact. Mob. Wearable Ubiquitous Technol., Vol. 7, No. 3, Article 110. Publication date: September 2023.


<footer>Proc. ACM Interact. Mob. Wearable Ubiquitous Technol., Vol. 7, No. 3, Article 110. Publication date: September 2023.</footer>
<header>110:8•Liang et</header>


110:8•Liang et


The detailed study,including experiment setup,results and explanation,are given in the Appendix.A.Here we summarize two major findings from the long-term activity data:


Activity intensity highly correlated with stress.By analyzing the Pearson coefficients between stress and each of the 39activity features,we observe that,the top-3features with the highest correlation are:the maximum value of in the direction of the z-axis,the number of activity frames,and the maximum number of point clouds.Note that these features describe the intensity of human activity over time.The result indicates that for some people,the higher the stress,the higher the intensity and frequency of human's activity,which corroborates with our empirical


High individual variation over stress features.We find that,the correlation between the same feature and stress,i.e.,the impact of the feature,exhibits significant variation among different subjects.Quantitatively,65.9%of the correlations differ significantly among individuals.The result inspires us to use personalized models in mmStressNet to infer human stress


To sum up,our analysis confirms the correlation between human activity and stress,which indicates the feasibility of distilling stress from daily activities (In Sec.6.1.1,we show that the proposed mmStress indeed pays attention to displacement activities).On the other hand,the relationship varies significantly across different individuals,which leads to poor performance of traditional machine learning models with hand-crafted features (like SVM or XGBoost,details in Sec.6.1.1).The findings motivate the design of mmStress,a custom-designed deep neural network to extract human activity features and classify stress autonomously in


# 4MMSTRESS DESIGN


Fig.5illustrates the architecture of mmStress.The system uses FMCW signals to sense human activity,i.e.,capturing the signals reflected by the human body and reverse-engineering it to derive human activity data so as to infer human stress levels.The mmStress system can be divided into four main parts:


(1)Signal Capture and Processing.First,mmStress emits FMCW signals with an FMCW radar operating at 60GHz mmWave band.Then mmStress receives and processes the reflected signal modulated by human activities,and thus generates human point cloud and trajectory,along with the the time stamps of each human activity.The point cloud describes the most active coordinates of the human body,and the trajectory is calculated by the weighted center of the clustered point cloud and the tracking algorithm,which describes the position of the person in space.
(2)Data Pre-Processing.We discard the point clouds with too low confidence and calibrate.Besides,we remove the redundant position coordinates generated by the clustering algorithm in the trajectories.
(3)mmStressNet.Then mmStress uses a custom-designed neural network called mmStressNet,which analyzes the differences in human activities under different stress levels,so as to infer subjects'stress.
(4)Solution for Stress-Data Distribution Imbalance.We adopt the post-hoc logit adjustment procedure [63]to solve the problem that most of the predicted labels fall into the majority


We proceed to detail these design modules one by


# 4.1Signal Capture and Processing


Human activities are usually defined as what a person does at a certain time and position.To get the activity information,we first capture the echoes of the FMCW signal reflected off from a human subject,using a modified TI IWR6843ODS mmWave radar.We then analyze the signal and derive point clouds through widely-used signal processing algorithms such as Range-FFT and Capon Beamforming [34].Then,we use clustering and prediction algorithms including the Extended Kalman filter (EKF)on the point cloud to generate human trajectories [31,32].Finally,we annotate the timestamp with the trajectory and the point cloud frame.The details can be found in Sec.5.3.In this way,we get the three features for describing a human activity,i.e.,timestamp,position (from the


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:9</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:9




Fig.5.Overview of mmStress design.The system uses mmWave FMCW radio to extract human activity data,and transform it into representation in terms of time,trajectories,and point clouds.These data,after pre-processing,is fed into the mmStressNet,which analyzes changes in human activities to infer stress levels.




Fig.6.The illustration of pruning erroneous position coordinates in the trajectory.The clustering algorithm generates two clusters:the real one c2,1and the redundant one $c_{2,2}$.mmStress chooses the position coordinate c2,1that is closest to the trajectory coordinate in the previous frame (T1)as part of the trajectory T2in the current frame,following Alg.1.


trajectory),and the activity itself (represented by the point cloud).However,before we feed the data into the mmStressNet,we need to filter out or correct the erroneous data,enhance the data quality of human activity features,and normalize them as detailed in the following.


# 4.2Feature Pre-Processing


4.2.1Pre-Processing Point Cloud.Note that each point in a point cloud is in the form of spherical coordinate,(range,azimuth,elevation,velocity).In order to facilitate subsequent data analysis and also to perform data enhancement on the point cloud features,we convert it into a Cartesian coordinate system.In particular,we deem the radar antenna as the origin and compute the point cloud coordinates projection on the ground (xg,yg,zg).Then,we remove the point clouds that are too close or too far from the radar,as they are usually ghost generated by the unavoidable noise [75].To enable the network to perceive the coordinate changes of human activity from


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.</footer>
<header>110:10•Liang et al.</header>


110:10•Liang et al.


|Algorithm1Ensure the trajectoriesgenerated byhumanactivityare continuousand unique.|
|:---|
|Require:All position coordinates present in the human activity Cn,m·|
|Ensure:The sequence{T1,..·，Tn} corresponding to theunique trajectory in the timeperiod.|
|1:fori=1;i|
|2: forj=1;i|
|3: D(ci,j）←lci,j-Ti-1ll2|
|4: end for|
|5: Ti←argmin[D(ci,j)]|
|6:endfor|



two different spaces,we retain the Cartesian coordinates of the point cloud in the room and the coordinates of a spherical coordinate with the radar antenna as the origin.Together with the radial velocity,we retain 7features for each frame of the point cloud.


4.2.2Pre-Processing Trajectory.The trajectory consists of the position coordinates generated from the point clouds for each frame.As we remove some poor-quality point clouds in the previous subsection,we need to remove the corresponding position coordinates so as to ensure trajectory consistence.However,the difficulty lies in that,due to the limited arithmetic power of the RF board,the clustering of point clouds often produces redundant position coordinates,when there is a sudden increase in the magnitude of human activity,such as the position coordinate c2,2represented by the yellow dots shown in Fig.6.To ensure that the trajectories generated by human activity are continuous and unique,we use Algorithm 1to remove these redundant position coordinates.The idea of the algorithm is illustrated in Fig.6:(i)The coordinate c1are used as the position coordinate T1where the human activity starts. $(i i)$Assume that there are multiple position coordinates in one frame,such as c2,1and c2,2,we choose the position coordinate c2,1that is closest to the trajectory coordinate in the previous frame as part of the trajectory $T_{2}$in the current frame.Other position coordinates further away from the human activity position in the previous frame are in most cases redundant position coordinates due to incorrect clustering of the point cloud.(iii)Until the traversal of the activity position for that time period is completed,at which the algorithm generates the unique trajectory sequence $\{T_{1},\:\cdots,\:T_{n}\}$of the human activity in that period.We keep 9attributes for each frame,which are coordinates indicating the person in space,velocity,and acceleration.


# 4.3mmStressNet Design


As shown before,the ambiguity of mmWave sensing data,together with the latent relationship between human activity and stress,prevents us from establishing a straightforward mapping of the two.In particular,we use conventional machine learning methods such as SVM and XGBoost and common time series neural networks such as GRU and LSTM (details in Sec.6.2.2),but none of them achieves satisfactory results.To handle the issue,we propose mmStressNet,a deep neural network that predicts stress by learning human daily activity as shown in Fig.7.Here we first introduce the overall structure of mmStress and then proceed to each module.


4.3.1Overview of mmStressNet.As shown in Fig.7,mmStressNet can be divided into three main modules,the Dimension Upgrading Module,the global view module,and the partial view module.The functions of the three modules are summarized as:(i)To address the sparsity of the data,we increase the dimension of the data to expand the differences of the activity frames while adding optimizable parameters for each subsequent module.(ii)Since the specific activities of people under different stress levels are submerged in the daily activity sequences,the global view module aims to identify as many as possible activity frames related to the stress level from those dispersed in the activity sequences.In this way,the model's sensitivity to stress-related activities is improved.(iii)The identified activity frames,however,may associate with multiple stress levels.Therefore,the partial view


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:11</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:11




Fig.7.Structure of mmStressNet.Input of mmStressNet is indeterminate length sequences including time,trajectory,and point cloud.The data is first processed by the dimension upgrading module,so as to increase the differences between activity frames.Then it is fed into the feature extractor,which is consisted of the global view module and the partial view module.The data imbalance resolver solves the problem of model accuracy degradation caused by stress mostly distributed at the low level.The final output is three levels of stress.


module analyzes the continuity of the activity to remove these excess introduced activity frames that are not related to the stress level.In this way,the model's accuracy in inferring stress is improved.


4.3.2Dimension Upgrading Module.Due to the sparsity of the point cloud generated by mmWave radios,the original point cloud properties are not sufficient to describe the fine-grained changes caused by human activities.Moreover,the three features we define to describe human activities,i.e.,time,trajectory,and point cloud,are not enough for subsequent feature extractors to distinguish activities and establish relationships between activities and stress.


There are two common ways to solve the sparsity of human activity data:(i)smooth interpolation,i.e.,using dense point clouds generated by other devices such as LiDAR [57]and cameras [102]as an aid;(ii)increasing the dimension of data to obtain more correlation features for several consecutive activity frames [30].However,the first scheme is not applicable in mmStress,as it introduces additional deployment of optical sensors in the home environment,which raises privacy concerns.


Thus,we adopt the second approach and design the Dimension Upgrading Module.The goal is to upgrade the dimension of human activities features to amplify the differences among activity features,increase the optimization parameters and enhance the fitting ability of the neural network [53].In particular,we define a set of activity features to be an N× Csequence of variable length (Nis the sequence length and Cis the number of channels).Inspired by ResNet [27],we use a 1× 1convolution kernel to upgrade the dimension of activity features.As shown in Fig.7,the number of channels for time,trajectory,and point cloud are up-dimensionalized from 5,9,and 160to 1024in this module,respectively.The reason for up-dimensioning the number of channels to 1024is that when we try a lower number of channels,it does not work well for stress inference;and when a higher number of channels is used,the accuracy of stress inference doesn't improve,but slow down the model training.After feature fusion,we obtain a set of abstract active sequences $\{a_{1},\cdots\}$,an}(where nis the length of the activity sequence).


4.3.3Global View Module.The global view module is part of the feature extractor in mmStressNet and serves to extract all possible activity frames associated with the subject's current stress level,from the global view


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.</footer>
<header>110:12•Liang et al.</header>


110:12•Liang et al.




Fig.8.Illustration of the effect of global and partial view modules.The blue and red dashed boxes represent the receptive field of the global view module and partial view module,respectively.


of the activity sequence.Recall that human activity data is denoted as variable-length time-series,and one straightforward idea is to use the RNN such as LSTM and GRU to process time-series sequences.However,we find the approach not feasible because the conventional RNN is unable to establish the relationship between two segments of activity frames that span a large time window.For instance,in a set of activity sequences,the nth -(n+20)th frames represent a displacement activity submerged in other daily activities,and the activity sequence from (n+1000)th frame to (n+1020)th frame is similar to the previous nth frame -(n+20)th frame.The two important displacement activities will not be related as RNN usually forgets too early activities.


In contrast,in the multi-head attention [91]view,the distance between any two activity frames in the sequence is 1.Taking the data in the previous paragraph as an example,the displacement activity of nthframe -(n+20)thframe is directly related to the activity of (n+1000)thframe to (n+1020)thframe,and there is no forgetting.The activity frames corresponding to this stress level are identified as many as possible.Therefore,we adopt multi-head attention to link all activity frames of the sequence $\{a_{1},\;,\cdots,\;a_{n}\}$,as shown in Equation 1:


$$A t t e n t i o n_{a}\left(Q_{a},K_{a},V_{a}\right)=s o f t m a x\left(\frac{Q_{a}K_{a}^{T}}{\sqrt{d_{k}}}\right)V_{a}$$


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.



<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:13</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:13


whereQa,Ka,Vaare obtained by multiplying the sequence $\left\{a_{1},\cdots,a_{n}\right\}$by the transformation matricesWQ,WK,WVof trainable parameters,respectively,and dkis the sequence length of Ka.Qaand Kawould match each other to calculate the correlation,so the activity frames with high relevance are linked in the activity sequence.Then,after the training of the neural network,the activity frames that are associated with the stress level would be given the matrices WQ,WK,WVwith larger weights.Finally,Qaand $K_{a}$are multiplied as the weights of the activity frame information Va,among which the activity frames that are most relevant to the stress level and have similar activity frames have the largest weights.


As an example,in Fig.8,we simplify the human activity into high-stress activity and non-high-stress activity,which are represented by a smiley face and a frustrated face above the activity frame,respectively.We take the displacement activity generated when extracting high stress as an example,and the theory can be analogized to extract the activity corresponding to low and medium stress.The multi-head attention uses the information extracted from the activity frames $V_{a}$to identify all stress-related activity frames as much as possible,such as (n+500)thframe -(n+801)thframe in the blue dotted box.In addition,it removes activity frames that are not stress-related and have no similarity to the activity in the sequence,e.g.(n+900)thframe. $Q_{a}K_{a}^{T}$ compares the similarity of all activity frames,so some frames that are not related to stress but have similar activities are also given weights.This module serves to improve the sensitivity of the model to stress-related activities,however inevitably some erroneous activity frames are introduced.which will be eliminated in the partial view module.After processing by the global view module,we obtain the more informative sequence of activities {ˆa1,···,ˆan}.


4.3.4Partial View Module.After obtaining the sequence {ˆa1,···,ˆan},we need to eliminate the wrong activity frames introduced in excess by the global view module.In particular,we find that some activity frames in the sequence have a weak association with the stress level,but they are very similar to other stress-related activity frames.We remove them based on an observation that the displacement activity is usually a continuous motion.Thus,if an activity frame is an independent frame and its surrounding activities are not related to the stress level,it can be considered unrelated to the stress level;otherwise,if there are multiple stress-related activity frames around it,it is more likely part of the displacement activity.As an example,in Fig.8,the nthframe is an incidental activity that is similar to the (n+500)thframe.Through continuity analysis by the partial view module,the frame is found stress-unrelated and thus is removed.


Therefore,we can exclude the interference of such activity frames by examining the continuity of the activity.In the partial view module,we use dilated causal convolutions [6]to analyze human activities of indeterminate lengths using its variable-length time window.Causal convolution ensures that the data are not leaked into history.In addition,the dilation convolution uses the editable parameter dilationto obtain information across different time scales on different hidden layers as shown in Fig.7.Eventually,the sequence {ˆa1,···,ˆan}is processed by this module and successive activity frames related to the stress level are in the red dotted line in Fig.8.After training,the network considers the person to be under this stress level if a similar activity sequence is recognized within a certain period.In addition,due to the variable length of activity sequences,we also use residual block [6]to avoid possible gradient disappearance caused by the deep network structures.After processing by the partial view module,we get the sequence, $\{a^{*}{}_{1},\cdots,a^{*}{}_{n}\},$with extracted features,and we take the last unit of that sequence,a∗n,as the output of the feature extractor.Then,after processing in the fully connected layer,we get the logits,a∗.


# 4.4Solutions for Stress-Data Imbalance


Since our data comes from the daily behavioral activities of people,there is unbalanced distribution in the dataset we have collected (data from the Garmin watch stress label).As shown in Fig.9,we analyze the distribution of stress levels,with low,medium,and high stress accounting for 55.0%,30.76%,and 14.34%,respectively.If we


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.</footer>
<header>110:14•Liang et al.</header>


110:14•Liang et al.




Fig.9.The proportion of each stress level in the stress data generated by all volunteers.


take conventional approaches in deep learning training,we may finally obtain high accuracy but most of the predicted results may fall into the majority class while the minority classes are confused with each other.


To handle the issue,recent studies have used either additional datasets [99]for training or linear interpolation of samples to generate the minority class of data [14].Considering the scarcity of mmWave datasets of monitoring human activities over long periods,and the complexity of human activities,we take a different approach,which requires no extra data but adapts loss function to address the stress-data imbalance.In particular,we utilize the post-hoc logit adjustment procedure [63]in the model training and test process.The main idea of the logit adjustment procedure is to incorporate the prior frequency of occurrence of stress levels P (s)in the training set into the softmax cross-entropy loss.When there is no distribution imbalance,the softmax cross-entropy loss tends to pursue the overall accuracy of the model.However,when the distribution of stress labels is no longer balanced and low-stress labels dominate the data,the predictions would eventually fall mostly into the low-stress class as the softmax cross-entropy continues to pursue the overall accuracy.The logit adjustment procedure gives weight to the accuracy of each level of stress prediction so that the accuracy of each class is re-balanced.


Before model training,we need to make sure that the training set and the test set have the same data distribution.For this classifier to achieve an equilibrium optimal prediction result for each stress level,Equation 2needs to be satisfied:


$${a g g m a x}_{s\in\ L}_s{}f}__{s}^^{*}={a r g m a x}_{_\sub\substack{{s\\in\[L]}}}\mathbb{P}^{b a l}\left(s\mid a\right),$$





where sis the stress level,Lis the number of pressure levels,f∗is the neural network that satisfies to reach a balanced optimum for each stress level,and argmaxs∈[L]Pbal(s|a)represents the optimization process of obtaining the predicted stress level sgiven the activity data aand equalizing (multiplying by the respective weights)the predicted stress level s.


In Sec.4.3.4,we define logits as $a^{*}$,and since logits need to be activated by a softmax activation layer,
where Softmax(a∗)=ea∗
�L
l=1
a∗.It can be inferred that $\mathbb{P}^{b a l}\left(s\mid a\right)\propto e x p\left(a^{*}\right)$.Furthermore,since $\mathbb{P}^{b a l}\left(s\ a\right)\infty$ $\mathbb{P}\left(s\mid a\right)/\mathbb{P}\left(s\right)$,where P (s)is the probability of occurrence of each stress level. $\mathbb{P}\left(s\mid a\right)$is the conditional probability of the predicted stress level given the training activity data a,then we can obtain Equation 3:


$${a g g m a x}_{s\in[L]}\mathbb{E}^{b a l}\left(s\mid a\right)={a r g m a x}_{s\in[L]}{e x p}\left(a^{*}\right)/\mathbb{P}\left(s\right)={a r g m a x}_{s\in[L]}a^{*}-{l n}\mathbb{P}\left(s\right)$$





We can calculate the prior distribution of stress levels P (s)before the model training,and subtract $l n\mathbb{P}\left(s\right)$from the logits obtained in the test set of the neural network to get the balanced optimal stress prediction result.


Proc.ACM Interact.Mob.Wearable Ubiqui


e 110.Publication date:September 2023.
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:15</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:15


Table 1.Configuration of parameters for the global view module and the partial view module.


<table><tr><td colspan="2">GlobalViewModule</td><td colspan="2">PartialViewModule</td></tr><tr><td>Input Channels</td><td>1024</td><td>Input Channels</td><td>1024</td></tr><tr><td>HeadNumber</td><td>2</td><td>Layer Number</td><td>4</td></tr><tr><td>LayerNumber</td><td>8</td><td>HiddenLayerChannels</td><td>[1024，1024,1024，2048]</td></tr><tr><td>FeedForwardChannels</td><td>2048</td><td>Kernal Size</td><td>4</td></tr><tr><td>Output Channels</td><td>1024</td><td>Dilation</td><td>[1,2,4,8]</td></tr><tr><td></td><td></td><td>Output Channels</td><td>2048</td></tr></table>


# 4.5mmStressNet Configurations


The configuration parameters for the global view module and the partial view module are shown in Table 1.To handle the stress-data imbalance issue in Sec.4.4,our loss function is softmax cross-entropy loss [41]as shown in Equation 4:


$$L(x)=-{\ g}{p}{}_{s}(a)=-{\operatorname{l o g}}\frac{e x p\left(a_{s}\right)}{\sum_{l=1}^{L}e x p\left(a_{c}\right)}$$





where ais the output vector,sis the ground truth stress label,and Lis the number of stress level.We use softmax [10]as the activation function of the fully connected layer and start training with a learning rate of 10−5and weight decay of 10−4using the AdamW optimizer [55]with $\left(\beta_{1},\beta_{2}\right)=\left(0.9,0.999\right)$.


# 5IMPLEMENTATION


# 5.1Hardware and Software


5.1.1Hardware.We modify the widely used mmWave radar TI IWR6843ODS as shown in Fig.10(a).RF board retains the data processing,transmission and power management-related chips,and adjusts their position.We reduce the number of pins to 20(as marked $\mathrm{b y}$red lines in Fig.10(a))to retain the communication and power supply functions for reducing its size as much as possible.In addition,to facilitate real-time data uploading from the radar deployed in the volunteers'homes,we create a data transmission board using Wi-Fi.The base of the data transmission board is adapted to the pins of the RF board (as in the right part in Fig.10(b)).The switch on the left in Fig.10(b)controls whether the data transfer is via USB serial or $\mathrm{W i-}F i,$and the switch on the right side controls the switch between the flash mode and function mode of the RF board.The Wi-Fi module's serial pins are connected to the serial pins of the RF board to communicate by way of pass-through.The two boards are stitched together to form our human daily activity collection device.The RF board is responsible for processing the mmWave signals reflected from the human body,i.e.,generating trajectories and point clouds.The data transmission board transmits these data to our cloud server in an anonymous and encrypted manner.


In addition,to better accommodate the device into the home environment and to facilitate installation,we use 3D printing to create a shell.We ask each volunteer to install the device in the centre of a wall or at a corner,2mabove the floor with a tilt angle of 15°.Considering that the area of houses rented by volunteers is less than 4m× 5mwith the main layout of tables,chairs,beds and computers as shown in Fig.10(c),we set the maximum detectable range of the radar to 7m.We test the average SNR of the radar-detecting human at various angles and ranges in a space of 4m× 7mwhile maintaining the same radar mounting height and inclination conditions as in the previous.The results are shown in Fig.11,which indicates that our radar is able to detect a valid target in the volunteers'home environment,where the radar manufacturer [34]illustrates that detecting a target reflected signal with the SNR greater than 12dBgenerates the valid point clouds.Also,as the IWR6843ODS has


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.</footer>
<header>110:16•Liang et</header>


110:16•Liang et




(a)Modified radar Radio Frequency (RF)




(b)Additional radar data transmission




(c)Respresentive volunteer's room layout and mmWave radar deployment




(d)mmWave radar deployment in volunteer


Fig.10.Modified mmWave radar sensor based on IWR 6843ODS and a showcase of its deployment in a volunteer's apartment.We mark major radar modifications with red line


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:17</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:17




Fig.11.SNR (dB)measured in a space of 4m×


an azimuthal field of view (FoV)of 120°,we adjust the azimuth angle of the sensor so that more than 95%of the volunteers'daily activity is within the Line of Sight (LoS)area of the sensor as shown in Fig.10(c)and


5.1.2Software.We use TI's CCSTUDIO [33]to complete the firmware modification and compilation.In addition,we deploy MySQL 8.0[61]on the Tencent Cloud server for data transfer and storage.We use Python scripts to align human activities with stress data and complete pre-processing of point clouds and trajectories.We also build the neural network mmStressNet based on PyTorch framework [73],which is trained on a server running Ubuntu 16.0with a Tesla K80


# 5.2Participants


We recruit 10volunteers including 8males and 2females,aged from 23to 29(with height from 158to 188cmand weight from 48to 76kg),from various industries.It is noteworthy that all volunteers follow their daily commuting and activity habits,which ensures data integrity.To fully describe a human activity,three types of data are needed,i.e.,time,position,and action.In particular,we use the above mmWave radar device to generate point clouds and trajectories describing human action and position,respectively.The corresponding timestamps are also recorded.To avoid interference from other persons,we delete the activity data if more than one person is present.We collect data from 10volunteers for 4weeks,8of them return valid data,and the other 2volunteers lost a lot of data due to network problems and incorrect watch-wearing.Among the 8volunteers who return valid data,1of them discontinue the experiment after 1week due to his


# 5.3Subject Daily Activity Collection


5.3.1Point Cloud Generation.The mmWave radar uses FMCW technology to transmit electromagnetic waves with linearly-modulated frequencies,and the transmitted signal is mixed with the received signal,which results in a mixed-frequency signal.Following conventional FMCW signal processing technologies[31,32,34,83],we


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>110:18•Liang et</header>


110:18•Liang et


derive the point cloud.(i)We do range-FFT on the mixed signals of each chirp and antenna to get the range spectrum,and then use static clutter removal to filter out static objects in space,including furniture like tables and beds [34].(ii)The Capon beamforming [84]is applied on this spectrum to generate the range-azimuth matrix [34].(iii)To further filter out the noise and get the detected points,the two-pass cell averaging smallest of constant false alarm rate algorithm (CASO-CFAR)[1]is executed on this matrix [34].CFAR-CASO is more effective in detecting weak targets in real home environments with noise [11],compared to CA-CFAR,which performs poorly in non-uniform noise,and CAGO-CFAR,which has difficulty detecting weak targets [1].(iiii)Capon beamforming is used on each detection point of the range spectrum to obtain the elevation spectrum,so that we can get a range-azimuth-elevation 3D point cloud [34].The doppler-FFT is applied for all detected point and used antennas to calculate the point cloud doppler (radial


Before feeding the data into the neural network,the data structure needs to be unified.To keep the effective point clouds as many as possible,we set the number of point clouds per frame to 20.If the number of point clouds in each frame is greater than 20,the 20point clouds with higher SNR are retained;Otherwise,the point clouds present in this frame are copied sequentially to the end of the point cloud sequence until the number of point clouds in this frame reaches


5.3.2Trajectory Tracking.To continuously track the trajectory of human activities,The basic idea is to continuously update the point cloud centroid and the matching of the trajectory.We use TI's Gtrack Library [31,32]for continuous tracking of human activity,and modify for the single person at the home scenario in Sec.4.2.The Gtrack algorithm for clustered tracking of point clouds proceeds as follows:


(1)For the first set of valid point clouds (see Step (3)for the validity check of the point clouds),we perform a weighted clustering based on the SNR of the point clouds and calculate their centroid as the starting position,and state of the trajectory.
(2)We use the extended Kalman filter to estimate the position of the point clouds centroid at the time (n)based on the position and state of the trajectory at the time (n -1)and the process covariance matrix.
(3)For the point cloud at the time (n),we first check its validity.Based on the previous configuration,we check that the number of point clouds is sufficient,that the coordinates of the point clouds are within the set space,that the radial velocity of the point clouds is within a reasonable range,and that the SNR of the point clouds is valid.
(4)The program checks that the surrounding point clouds are within the reasonable Mahalanobis distance from the predicted centroid.These point clouds are weighted based on the SNR to calculate a new centroid.The point cloud calculation produces the centroid and the centroid based on the time (n -1)predictions are weighted and compromised to generate the position and state of the trajectory at time n,and a new error covariance estimate is calculated.The procedure then continues from Step (2).
(5)For point clouds that are not matched to an existing trajectory,the program would attempt to cluster these point clouds into new trajectories and would continue with Step (1).If the conditions for generating new trajectories cannot be met,these point clouds would be


The point cloud and trajectory data generated by the mmWave radar are uploaded anonymously via Wi-Fi to an encrypted cloud server through the volunteers'home routers.We set the frequency at which the radar transmits and processes signal to 10Hz,which means that the radar can describe up to ten frames per second of human activity.Each of these processed frames represents a snapshot of the person's activities at that moment,including the position and trend of human


In Sec.5.1.1,we illustrate that the volunteers live alone and that the radar detection capability is sufficient to cover the rooms rented by the volunteers.Our survey shows that volunteers spend most of their time in their rooms during the weekdays,except for work,and on average spend more than 11hours a day in their rooms,except for weekends.Due to the static filtering algorithm running on the mmWave radar,the radar does not


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:19</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:19


output information about the volunteer's activity when the volunteer remains still (e.g.during periods of sleep).The reason for discarding this part of the information is that at this time,the person is usually in a relaxed state and the stress level is low in most cases,which is not helpful for our model


After filtering the point cloud and trajectory data in Sec.4.2,we select all half hours with an activity frame count greater than two as the valid time slices.In the end,the average effective activity time per person per day we used was more than seven hours.We use non-overlapping time windows for both training and validation.In total,we collect 4,648,029mmWave sensing data frames,corresponding to over 1,200hours of activity data and 145,186stress values.After the data acquisition phase,all the data would be used to train mmStressNet to obtain a model for distilling stress from daily human


# 5.4Subject Stress Condition Collection


We use smartwatches to monitor subject stress levels,which serve as supervision labels in model training and ground truth in evaluation.We note that while one common way to get ground truth is via questionnaires,we can not rely on them due to the following reasons:


(1)The experiment requires volunteers to generate a stress label every half hour.This is feasible for short-term monitoring,whereas for long-term monitoring,excessive questionnaire filling often leads to volunteers becoming bored and returning homogeneous and unreliable [9,47].
(2)For many practical daily life scenarios,such as commute preparation,sleep,etc.,it is not possible to ask volunteers to generate stress labels through questionnaires.
(3)Filling out the questionnaire itself is an action,which would interfere with the original human daily activity and cause stress prediction


Therefore,we use a widely-used COTS smartwatch Garmin venu sq smartwatch [44]to generate stress labels.The smartwatch algorithm calculates the stress mainly from the HRV measured by the equipped photoplethysmography (PPG)and integrates human activities.The previous studies [72,79]demonstrate high accuracy measured by the Garmin watch.In particular,the algorithm generates a stress value every 3minutes with a score range of 0-100.The higher the score,the higher the person's stress level is [45].Unlike the criteria provided by Garmin that classifies a stress value greater than 75as high,we find that volunteers generate stress scores greater than 75rarely during data collection,accounting for only 2%of the overall stress-related activity events.The previous study [4]concludes that stress scores in the range of 26-50are normal for everyday life and that high-stress scores above 50are harmful to people.Thus in our experiments,we follow this stress classification criterion and classify human stress into 3levels:low (0-25),medium (26-50),and high (51-100).In Sec.3,we conclude that the stress level is usually stable in 1hour.Because we collect data with a small percentage of medium and high stress,we set the data collection window to 30minutes to increase the number of samples,and the stress label is set to the average over 30


# 6EVALUATION


The evaluation of mmStress is divided into two main parts.In Sec.6.1,we validate the performance of mmStress under various conditions;In Sec.6.2,we evaluate the individual module design inside mmStress.Because the data we collect is continuous in time,in general,for a given sequence of volunteer activities,we use the first 75%of that sequence as the training set and the remaining 25%as the test set.For example,if we collect 4weeks of activity data from a volunteer,we use the first 3weeks of activity data as the training set and the remaining 1week of activity data as the test


Evaluation metrics:We use accuracy,precision,recall,and F1-score to assess the model's correctness,sensitivity,and overall performance,which are shown in Equations 8-10,where TP,FP,FNrepresent the true positive,false positive and false negative,and Srepresents the stress level,which is classified as low,medium,


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>110:20•Liang et al.</header>


110:20•Liang et al.




Fig.12.Stress classification results using personalized models.


and high.In addition,to illustrate the effect of solving the unbalanced distribution of stress labels (Sec.4.4),we use macro-average to calculate the arithmetic mean of precision,recall,and F1-score for each stress level to obtain Macro-Precision,Macro-Recall,and Macro-F1-score as shown in Equations 5-7,where P,R,and F denote precision,recall,and F1-score,respectively.


# 6.1System-Level Evaluation


Plow + Pmedium + Phigh Macro-Precison= 3


Rlow + Rmedium + Rhigh Macro-Recall= 3


$$\begin{aligned}{M a c r o-P r e c i s o n}&{{}=\frac{P_{l o w}+P_{m e d i u m}+P_{h i g h}}{3}}\\ {M a c r o-R e c a l l}&{{}=\frac{R_{l o w}+R_{m e d i u m}+R_{h i g h}}{3}}\\ {M a c r o-F1-s c o r e}&{{}=\frac{F_{l o w}+F_{m e d i u m}+F_{h i g h}}{3}}\\ {P r e c i s i o n_{S}}&{{}=\frac{T P_{S}}{T P_{S}+F P_{S}}}\\ {R e c a l l_{S}}&{{}=\frac{T P_{S}}{T P_{S}+F N_{S}}}\\ {F1-s c o r e_{S}}&{{}=\frac{2\times P r e c i s i o n_{S}\times R e c a l l_{S}}{P r e c i s i o n_{S}+R e c a l l_{S}}}\\ \end{aligned}$$


TPs Precisions = TPs + FPs


TPs Recalls TPs + FNs


2×Precisions×Recalls F1-scores= Precisions+Recalls




















6.1.1Overall Performance.Based on the setup and user study (Sec.3),we first evaluate the performance of mmStress with the personalized model and universal model,respectively.Then we compare mmStress against other methods,and finally,we use a case study to illustrate the effectiveness of mmStress in practice.


Personalized Model Evaluation.For personalized model evaluation,we divide each volunteer's data into training (75%)and test (25%)sets and build an individualized model using mmStressNet for each volunteer.Fig.12shows the performance of mmStress:the accuracy is in the range of 72.6%-100%,with a mean of 83.0%;Macro-F1-score is in the range of 71.2%-100%,with a mean of 78.8%;Macro-Precision is in the range of 71.2%-100%,and the average is 80.0%;Macro-Recall is in the range of 71.2%-100%,and the average is 80.2%.Among them,volunteer #3reaches 100%for all evaluation metrics.We find that his stress changes particularly smoothly,with


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.</footer>
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:21</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:21


Table 2.Comparison between the personalized model and the universal cross-validation model.The mean of each volunteer assessment values is used as the personalized model evaluation results.


Personalized Model
Universal Model
Accuracy (%)
83.0
68.0
Macro-F1-score (%)
78.8
61.1
Macro-Precision (%)
80.0
61.0
Macro-Recall (%)
80.2
64.2





Fig.13.Effect of the number of volunteers in the training set on the universal model.


only a very small amount of high-stress labels present in the dataset.The volunteer lives in a staff dormitory with a very regular activity pattern.


Universal Model Evaluation.Towards a more universal evaluation,we adopt the leave-one-subject-out (LOSO)policy by using the data of the ithvolunteer as the test set and the data of other volunteers as the training set.In this experiment,iis iterated from 1to 8,and the averages of evaluation metrics are given in Table 2.We find that the personalized model outperforms the LOSO model evaluation in all aspects,as behavioral activities vary widely across individuals,as we show in Sec.3.


However,we believe that a high-accuracy universal model can be achieved if increasing training data.To verify this hypothesis,we use the data of the ithvolunteer as the test set and increase the sample size of volunteers,gradually.For instance,for volunteer #1,the training set is from only volunteer #2at first,and then from volunteer $\#2-\#3,\ldots$,and finally from volunteers #2-#8.(The proportions of data provided by volunteers #1-#8are:20.68%,13.84%,1.13%,13.96%,14.43%,7.86%,13.81%,and 14.29%.)The results are shown in Fig.13,where the average F1-score of the universal model rises as the sample increases.


Comparison With Other Methods.Here we compare mmStress against traditional temporal sequence processing methods,and against the state-of-the-art WiStress [26]later in Sec.6.1.2.In particular,we first manually extract features as introduced in Sec.3,and use them to train traditional machine learning models,i.e.,Linear SVM and XG boost.In addition,we also train two commonly used temporal neural networks,GRU and LSTM.For all comparison methods,we use the personalized model for each volunteer and the Macro-F1-score as the evaluation metrics.The performance of each method is shown in Fig.14,from which we have the following observations:(i)The traditional non-deep learning models have the lowest Macro-F1-Score,with the average value of 23.4%for SVM,and 57.6%for XG Boost,respectively.The results indicate that the performance of manually extracted features is worse than that of the neural networks.This is because the correlations between data are necessarily


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.</footer>
<header>110:22•Liang et</header>


110:22•Liang et




Fig.14.Comparison between mmStress and several common traditional machine learning and deep learning methods.Evaluation metric is




Fig.15.mmStress's stress v.s.groundtruth


lost when features are manually extracted,especially for the long-time series model.Worse still,the extremely low accuracy of linear SVM validates that,there is no simple linear relationship between human displacement activities and stress changes.(ii)Among all deep-learning models,mmStress significantly outperforms the LSTM and GRU in this experiment,i.e.,with the average Macro-F1-Score of 78.8%for mmStress,65.0%for LSTM,and 65.1%for GRU.The reason lies in that,mmStress is able to find connections between cross-frame data and capture the effects of successive actions on stress.In particular,the residual blocks in mmStressNet are also able to mitigate


l.7,No.3,Article 110.Publication date:September


Proc.ACM Interact.Mob.Wearable Ubiquitous
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:23</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:23


Table 3.Stress classification under two activity scenarios.'N/A'means no results,as WiStress depends on accurate heartbeat information,which cannot be derived under free activity scenario.


<table><tr><td></td><td colspan="2">Quasi-Static</td><td colspan="2">FreeActivity</td></tr><tr><td></td><td>mmStress</td><td>WiStress</td><td>mmStress</td><td>WiStress</td></tr><tr><td>Accuracy</td><td>82.6%</td><td>86.1%</td><td>83.0%</td><td>N/A</td></tr><tr><td>Macro-F1-score</td><td>75.3%</td><td>85.2%</td><td>78.8%</td><td>N/A</td></tr></table>


the gradient disappearance when training long sequences of data,which is a deficiency present in LSTM and GRU.


Fig.15showcases the stress variation (both the ground truth and mmStress's prediction)of volunteer #1with low stress (with the least work overtime from telephone interview)and #5with high stress.We find that mmStress can constantly and accurately monitor subjects'stress changes.Quantitatively,the average high-/medium-/low-stress classification errors are $27.1\%$23.4%,and 9.0%,respectively.


6.1.2Impact of Human Activity Intensity.Here we compare mmStress against WiStress,which infers human stress from heartbeat under quasi-static scenarios.In particular,we recruit 3new volunteers and infer their stress levels under the quasi-stationary state,with mmStress and WiStress,respectively.In the quasi-static scenario,volunteers work at the desk,with minor activities including moving the mouse and typing,etc.,which only disturb the chest the least.The experiment lasts seven days,and the results are given in Table 3,from which we have the following observations:(i)WiStress achieves an accuracy of 86.1%and a Macro-F1-Score of 85.2%,consistent with the earlier study [26].(ii)mmStress has a slightly lower average accuracy of 82.6%and a lower Macro-F1-score of 75.3%.The reason lies in that,displacement activities caused by high stress are not exhibited clearly,as human activity intensity is limited or cannot be described by trajectories and point clouds due to the reduced activity amplitude.Therefore,we note again that mmStress complements WiStress in moving scenarios,a more common and normal case in daily life.


On the other hand,under free-activity scenarios,mmStress is more effective in monitoring human stress and the accuracy is maintained at more than 80%,and the Macro-F1-score reaches 78.8%.The near equality of these two evaluated metrics represents the equal ability of mmStress to speculate on high and low stress,as the displacement activity induced by high stress can be executed by the person in its entirety.In contrast,WiStress could no longer generate valid stress prediction.Recall that WiStress depends on accurate estimation of heartbeat,i.e.,interbeat interval (IBI)and HRV.However,With the increase of the range and frequency of human activities,the error of WiStress for IBI extraction gradually increases,which leads to the inefficacy of WiStress.


In particular,we examine the accuracy of WiStress for IBI estimation at 3different activity intensities over 30minutes for 3participants.The results are shown in Fig.16,where static indicates that the human torso and limbs remain stationary;Quasi-Static indicates that only minimal activity is possible,such as moving the mouse and typing slowly in front of a computer,and the activity does not disturb the chest as much as possible;L-Activity means that people can engage in low-intensity activities,such as fast continuous flipping through documents and typing;M-Activity means that a medium level of physical activity can be performed,including shaking the body and shaking the legs.We find that simply shaking the leg and shaking the body in the seat (corresponding to the M-activity in Fig.16)can lead to an IBI estimation error greater than 150ms.In addition,during free activity,the mmWave sensor is usually not fully aligned with the body's chest cavity,and the heartbeat signal cannot be captured.


6.1.3Impact of Environment.To investigate the environmental adaptability of mmStress,we now repeat the experiment in Sec.6.1.2with volunteers in a different environment,in which we update the layout,readjust the


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.</footer>
<header>110:24•Liang et</header>


110:24•Liang et




Fig.16.The increased intensity of human activity leads to a larger IBI




Fig.17.Impact of environment change.E_new+means fine-tuning with few anew environment




Fig.18.mmStress under different


sensor position,and replace part of the test site as shown in Fig.18.The two experiment sites are a 2m× 2mworking cubicle and a 5m× 7moffice respectively.The experiment results are given in Fig.17.which shows that mmStress degrades a lot,i.e.,the accuracy,and the average Macro-F1-score,Macro-Precision,and Macro-Recall of all volunteers drop to 54.3%,47.9%,50.5%,and 51.6%,respectively.However,if we fine-tune mmStress with a small amount of activity data in the new environment (only 10%of the original training set),the accuracy of stress inference (marked as E_new+)is significantly improved.For instance,adding 1additional day of data collected in the new environment to seven days of data collected in the old environment set will result in a significant improvement:the average accuracy,Macro-F1-score,Macro-Precision,and Macro-Recall of all volunteers are improved to 75.0%,72.8%,83.2%,and


We analyze the results and find that:(i)The environment changes,including the corresponding mmWave radar installation position,furniture layout,and the relative position of human activities,which distort the raw mmWave signal distribution and lead to performance degradation.(ii)However,user activity habits will not change despite the environmental dynamics,and mmStress can still leverage the corresponding activity features from the data of the original environment.Therefore,only a small amount of activity data from the new environment is required for mmStress to remain


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:25</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:25




Fig.19.Ablation study of the impact of each activity feature:time (T),trajectory (TR)and point cloud


# 6.2Micro-benchmark Experiments




Fig.20.Ablation study of two feature extractors:the partial view (PV)and the global view module


6.2.1Impact of Activity Features.Here we evaluate the contribution of three features used in mmStress,i.e.,time (T),trajectory (TR)and point cloud (PC).In particular,we feed the features incrementally into mmStress,using the same long-term data set in Sec.6.1.1.We still use the personalized model and the mean of Macro-F1-score as the performance metric.The experiment results are given in Fig.19,from which we have the following observation:(i)Stress predictions using only time feature is greater than 33.3%on the personalized model,higher than random guesses.The result validates that stress usually shows a regular and periodic pattern,like stress accumulating with the hours of work.(ii)T&PCcombination is better than T&TR,because trajectory can only describe the human position and simple overall body activities,while point cloud can describe human motion in a more fine-grained way.(iii)The combination of two features (i.e.,T&TRor T&PC)cannot completely characterize human activities,as evidenced by that their accuracy is less than that of the three fusion.Overall,the integration of the three is necessary to completely describe the daily activities of people,and the inference of stress can reach the


6.2.2Impact of mmStress Feature Extractor.As shown in Fig.7,the feature extractor of mmStressNet is divided into two parts:the partial view module and the global view module.We now evaluate each module's effect separately,with the same setup as above.From the results in Fig.20,mmStressNet using only the partial view module or only the global view module achieves an accuracy of 63.3%and 68.1%,respectively,which are lower than 78.8%when the two are combined.When the feature extractor only retains one module,mmStressNet cannot exert its original ability,and the experiment results demonstrate the effectiveness of the two modules in the feature extractor of


In addition,we verify that the feature extractor of mmStressNet indeed pays attention to displacement activities.We ask a volunteer to repeat the experiment in Sec.6.1.2for 2hours.We use an extra smartphone camera to record the volunteer's activities.We select a segment of the activity sequences,feed it into the trained model,and output the attention values.We match each normalized attention value with the velocity,distance,and recorded images at the same time.The experiment result is given in Fig.21.We can find that most of the activity frames that mmStressNet focuses on undergoing an increase in activity velocity or distance,as marked in the black dashed line boxes,which is consistent with the finding that stress is positively correlated with activity intensity in Sec.3.We match these times of high normalized attention value with our recorded images and find that people were also performing some displacement activities at this time as indicated by the red dotted box in Fig.21.For


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>110:26•Liang et</header>


110:26•Liang et




Fig.21.mmStress's attention evolves over a period of time,which demonstrates that mmStress indeed pays attention to the displacement activities in order to classify stress


some non displacement activities with large moving distances,mmStressNet does not pay attention to it.For example,as shown in Fig.21,the volunteers in the blue dashed box is leaning back and looking


6.2.3Impact of Dimension Upgrading Module.To evaluate the usefulness of the dimension upgrading module,an experiment sets the channel numbers of the dimension upgrading module to 256,512,1024,and 2048and uses the average F1-score of personalized models as the result.The results are shown in Fig.22,where the Macro-F1-score reaches optimality when the number of convolution kernels of the module is 1024.If the number of convolution kernels of the module is increased further,the model is inevitably overfitted.The higher the number of convolution kernels,the more relationships between the activity frames,and when a suitable value is reached,the effect of sparse point clouds can be mitigated;conversely,if the number of convolution kernels is too high,it could lead to model overfitting


6.2.4Impact of Time Window Selection.Here we evaluate the impact of varying time window sizes,ranging from three to 30minutes,on the performance of mmStressNet.As shown in Fig.23,the performance of the network improves with the size of the time window until the time window reaches 30minutes.The increase in the time window would include more human activity to better establish the relationship between displacement activity and stress.However,exceeding a certain limit not only brings an increase in training time but mmStressNet is also unable to fit too long data.This leads to a decrease in model performance.Taking into account both training time and model performance,we set a time window of 30


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:27</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:27




Fig.22.Impact of the number of convolution kernels in Dimension Upgrade




Fig.23.Impact of time window


6.2.5Validation of Resolving Stress-Data Imbalance.Here we examine the effect of solving the unbalanced data distribution by mmStress's post-hoc logit adjustment procedure,under the same setup above.In particular,we find that the accuracy prediction Macro-F1-score is improved from 60.7%to 78.8%after using the post-hoc logit adjustment procedure.To illustrate the effect,We use the case of two representative volunteers shown in Fig.24.For volunteer #4,low stress is accurately handled even without the post-hoc logit adjustment procedure,as the low-stress data are the most abundant.However,the prediction for high and medium stress falls heavily into medium and low stress.For volunteer #5,it is hard to distinguish medium and high stress without adjustment.After applying the post-hoc logit adjustment procedure,the accuracy of both cases has been significantly improved,which demonstrates that mmStress can handle different kinds of data imbalance


# 7DISCUSSION


While mmStress yield promising results in distilling stress from human daily activities,there are the following issues to be further


Universal stress prediction model.Currently,our personalized model (one model for each subject)obtains high accuracy in long-term stress monitoring but degrades when apply to different subjects.We believe that training a model with much more data,i.e.,letting the model learn from huge and diverse human activity patterns would help to achieve a universal prediction ability,which we left for future


Stress monitoring for co-existing multiple subjects across multiple rooms.Currently,mmStress operates for only one person present at the same time,and cannot identify different people and monitor their stress separately.We plan to incorporate the ability of gait recognition [62]into mmStress to achieve stress monitoring in the workplace or family where multiple subjects co-exist.Limited by the sensing range and poor wall-penetration ability of mmWave radar,mmStress now captures the user's activity inside a room.To derive a complete record of the user's daily activity across different rooms (e.g.,living room,bedroom,etc.),we can deploy multiple mmWave sensors and form a sensing


Displacement activity caused by other factors.The triggers for displacement activities are complicated.For instance,thinking can cause face-scratching and fatigue can cause yawning.However,some studies show that these burdensome factors and stress are not independent of each other,but are interrelated.For example,thinking can lead to constant stress [64],and fatigue and stress often coexist [65].Moreover,in our experiment in Sec.3.1,MIST is based on the principle of inducing stress by making people think through the mental arithmetic task [20].However,monitoring human stress through displacement activity alone may not be appropriate for people with


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>110:28•Liang et</header>


110:28•Liang et




(a)Confusion matrix for volunteer #4with and without logit adjustment




Fig.24.Effect of the post-hoc logit adjustment procedure in solving the unbalanced data distribution issue.Confusion matrices for two volunteers with and without the post-hoc logit adjustment procedure are


limited mobility,such as bedridden patients,the elderly,etc.In future work,we can use mmWave to monitor more human health indicators such as respiration and HRV,in hope of making mmStress widely


Deriving stress ground-truth in the long-term experiment in real environments can be challenging.While questionnaires can provide valid results during the initial days of an experiment,their reliability may decrease over time,as volunteers become bored with repetitive questions.Complex physiological sensors,such as electrocardiograms (ECGs),can provide accurate measurements but may be burdensome to incorporate into daily routines.Smart bracelets and watches are well-suited for long-term monitoring,but their accuracy can be affected by physical activity [56].In our experiments,we ask volunteers to wear the Garmin watch for three days in advance.Additionally,psychological stress may not always be reflected in physiological signals.In future work,we plan to combine physiological information with subjective questionnaires to provide a comprehensive picture of an individual's


Extending to monitor other chronic diseases.mmStress exploits the link between daily activities and changes in stress,shedding light in this important direction.In addition,the development of some chronic diseases has a high correlation with stress,and we plan to explore the possibility of using a person's daily activity to predict early symptoms of chronic diseases in the


l.7,No.3,Article 110.Publication date:September


Proc.ACM Interact.Mob.Wearable Ubiquitous
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:29</header>


# 8CONCLUSION


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:29


In this paper,we present mmStress,which can infer human stress from sensing daily human activities in a nonintrusive way,using a contactless mmWave radar.mmStress explores the link between daily human behaviors and stress changes without restricting human movement,and custom-designs a deep-learning neural network to identify latent but stress-related activity features.The extensive evaluation demonstrates the effectiveness of mmStress,with the average accuracy of ∽80%for a one-month 8-person user study,under different environments and living habits.We believe mmStress,beyond stress monitoring in this work,also has the potential to help predict and manage other psychological and physical chronic diseases,like anxiety and depression prediction [8],and habit optimization for cardiovascular disease and type 2diabetes


# ACKNOWLEDGMENTS


The work is supported in part by the Funds for Creative Research Groups of China under Grant No.61921003,NSFC (61720106007)and the Youth Top Talent Support Program.Chenshu Wu is supported in part by NSFC under grant No.62222216and Hong Kong RGC ECS under grant


# REFERENCES


[1]Mohamed A.Abdel-Nabi,Karim G.Seddik,and El-Sayed A.El-Badawy.2012.Spiky sea clutter and constant false alarm rate processing in high-resolution maritime radar systems.In 2012International Conference on Computer and Communication Engineering (ICCCE).478–485.https://doi.org/10.1109/ICCCE.2012.6271233
[2]Aakriti Adhikari,Austin Hetherington,and Sanjib Sur.2021.mmFlow:Facilitating At-Home Spirometry with 5G Smart Devices.In 202118th Annual IEEE International Conference on Sensing,Communication,and Networking (SECON).1–9.https://doi.org/10.1109/SECON52354.2021.9491616
[3]Fadel Adib,Zach Kabelac,Dina Katabi,and Robert C Miller.2014.3D tracking via body radio reflections.In 11th USENIX Symposium on Networked Systems Design and Implementation (NSDI 14).317–329.
[4]Fatema Akbar.2021.Stress and Human-Computer Interaction at the Workplace:Unobtrusive Tracking With Wearable Sensors and Computer Logs.University of California,Irvine.
[5]Mohammed A Almazrouei,Ruth M Morgan,and Itiel E Dror.2022.A method to induce stress in human subjects in online research environments.Behavior Research Methods (2022),1–8.
[6]Shaojie Bai,J Zico Kolter,and Vladlen Koltun.2018.An empirical evaluation of generic convolutional and recurrent networks for sequence modeling.arXiv preprint arXiv:1803.01271(2018).
[7]Jorn Bakker,Mykola Pechenizkiy,and Natalia Sidorova.2011.What's Your Current Stress Level?Detection of Stress Patterns from GSR Sensor Data.In 2011IEEE 11th International Conference on Data Mining Workshops.573–580.https://doi.org/10.1109/ICDMW.2011.178
[8]Arnab Barua,Abdul Kadar Muhammad Masum,Erfanul Hoque Bahadur,Mohammad Robiul Alam,MAUZ Chowdhury,and Mohammed Shamsul Alam.2020.Human activity recognition in prognosis of depression using long short-term memory approach.International Journal of Advanced Science and Technology 29(2020),4998–5017.
[9]Liv Bixo,Janet L Cunningham,Lisa Ekselius,Caisa Öster,and Mia Ramklint.2021.'Sick and tired':Patients reported reasons for not participating in clinical psychiatric research.Health Expectations 24(2021),20–29.
[10]John Bridle.1989.Training stochastic model recognition algorithms as networks can lead to maximum mutual information estimation of parameters.Advances in neural information processing systems 2(1989).
[11]Long Cai,Xiaochuan Ma,Shefeng Yan,Chengpeng Hao,and Rongbo Wang.2010.Some Analysis of Fuzzy CAGO/SO CFAR Detector in Non-Gaussian Background.In 20102nd International Workshop on Intelligent Systems and Applications.1–4.https://doi.org/10.1109/IWISA.2010.5473461
[12]R.Castaldo,P.Melillo,U.Bracale,M.Caserta,M.Triassi,and L.Pecchia.2015.Acute mental stress assessment via short term HRV analysis in healthy adults:A systematic review with meta-analysis.Biomedical Signal Processing and Control 18(2015),370–377.https://doi.org/10.1016/j.bspc.2015.02.012
[13]Youngjun Cho,Nadia Bianchi-Berthouze,Simon J.Julier,and Nicolai Marquardt.2017.ThermSense:Smartphone-based breathing sensing platform using noncontact low-cost thermal camera.In 2017Seventh International Conference on Affective Computing and Intelligent Interaction Workshops and Demos (ACIIW).83–84.https://doi.org/10.1109/ACIIW.2017.8272593
[14]Hsin-Ping Chou,Shih-Chieh Chang,Jia-Yu Pan,Wei Wei,and Da-Cheng Juan.2020.Remix:rebalanced mixup.In European Conference on Computer Vision.Springer,


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>110:30•Liang et</header>


110:30•Liang et


[15]Matteo Ciman,Katarzyna Wac,and Ombretta Gaggi.2015.iSensestress:Assessing stress through human-smartphone interaction analysis.In 20159th International Conference on Pervasive Computing Technologies for Healthcare (PervasiveHealth).84–91.https://doi.org/10.4108/icst.pervasivehealth.2015.259280
[16]Sheldon Cohen,Peter J.Gianaros,and Stephen B.Manuck.2016.A Stage Model of Stress and Disease.Perspectives on Psychological Science 11,4(2016),456–463.https://doi.org/10.1177/1745691616646305arXiv:https://doi.org/10.1177/1745691616646305PMID:27474134.
[17]Sheldon Cohen,Denise Janicki-Deverts,and Gregory E.Miller.2007.Psychological Stress and Disease.JAMA 298,14(102007),1685–1687.https://doi.org/10.1001/jama.298.14.1685arXiv:https://jamanetwork.com/journals/jama/articlepdf/209083/jco70057_1685_1687.pdf
[18]Nicola Coppedè,Giuseppe Tarabella,Marco Villani,Davide Calestani,Salvatore Iannotta,and Andrea Zappettini.2014.Human stress monitoring through an organic cotton-fiber biosensor.Journal of Materials Chemistry B 2,34(2014),5620–5626.
[19]Ernest Dallé and Musa V Mabandla.2018.Early life stress,depression and Parkinson's disease:a new approach.Molecular brain 11,1(2018),1–13.[20]Katarina Dedovic,Robert Renwick,Najmeh Khalili Mahani,Veronika Engert,Sonia J Lupien,and Jens C Pruessner.2005.The Montreal Imaging Stress Task:using functional imaging to investigate the effects of perceiving and processing psychosocial stress in the human brain.Journal of Psychiatry and Neuroscience 30,5(2005),319–325.
[21]Paddy C Dempsey,Chuck E Matthews,S Ghazaleh Dashti,Aiden R Doherty,Audrey Bergouignan,Eline H Van Roekel,David W Dunstan,Nicholas J Wareham,Thomas E Yates,Katrien Wijndaele,et al.2020.Sedentary behavior and chronic disease:mechanisms and future directions.Journal of Physical Activity and Health 17,1(2020),52–61.
[22]Firdaus S Dhabhar.2018.The short-term stress response–Mother nature's mechanism for enhancing protection and performance under conditions of threat,challenge,and opportunity.Frontiers in neuroendocrinology 49(2018),175–192.
[23]Raihana Ferdous,Venet Osmani,and Oscar Mayora.2015.Smartphone app usage as a predictor of perceived stress levels at workplace.In 20159th International Conference on Pervasive Computing Technologies for Healthcare (PervasiveHealth).225–228.https://doi.org/10.4108/icst.pervasivehealth.2015.260192
[24]Grace Guan,Merav Mofaz,Gary Qian,Tal Patalon,Erez Shmueli,Dan Yamin,and Margaret L Brandeau.2022.Higher sensitivity monitoring of reactions to COVID-19vaccination using smartwatches.NPJ Digital Medicine 5,1(2022),140.
[25]Junchen Guo,Meng Jin,Yuan He,Weiguo Wang,and Yunhao Liu.2021.Dancing Waltz with Ghosts:Measuring Sub-Mm-Level 2D Rotor Orbit with a Single MmWave Radar.In Proceedings of the 20th International Conference on Information Processing in Sensor Networks (Co-Located with CPS-IoT Week 2021)(Nashville,TN,USA)(IPSN '21).Association for Computing Machinery,New York,NY,USA,77–92.https://doi.org/10.1145/3412382.3458258
[26]Unsoo Ha,Sohrab Madani,and Fadel Adib.2021.WiStress:Contactless Stress Monitoring Using Wireless Signals.Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.5,3,Article 103(sep 2021),37pages.https://doi.org/10.1145/3478121
[27]Kaiming He,Xiangyu Zhang,Shaoqing Ren,and Jian Sun.2016.Deep residual learning for image recognition.In Proceedings of the IEEE conference on computer vision and pattern recognition.770–778.
[28]Miriam I.Hehlmann,Brian Schwartz,Teresa Lutz,Juan Martín Gómez Penedo,Julian A.Rubel,and Wolfgang Lutz.2021.The Use of Digitally Assessed Stress Levels to Model Change Processes in CBT -A Feasibility Study on Seven Case Examples.Frontiers in Psychiatry 12(2021).https://doi.org/10.3389/fpsyt.2021.613085
[29]Xiyuan Hou,Yisi Liu,Olga Sourina,Yun Rui Eileen Tan,Lipo Wang,and Wolfgang Mueller-Wittig.2015.EEG Based Stress Monitoring.In 2015IEEE International Conference on Systems,Man,and Cybernetics.3110–3115.https://doi.org/10.1109/SMC.2015.540
[30]Che-Wei Hsu,Yu-Hsiang Huang,and Nen-Fu Huang.2022.Real-time Dragonfruit's Ripeness Classification System with Edge Computing Based on Convolution Neural Network.In 2022International Conference on Information Networking (ICOIN).IEEE,177–182.
[31]Texas Instruments.2021.Group Tracker Parameter Tuning Guide for the 3D People Counting Demo.https://dev.ti.com/tirex/explore/node?node=AHZY4H1u04B21l9zTRElvQ__VLyFKFf__LATEST
[32]Texas Instruments.2021.Tracking radar targets with multiple reflection points.https://dev.ti.com/tirex/explore/node?node=AM.QUGqhwdBqRvUeI98JuA__VLyFKFf__LATEST
[33]Texas Instruments.2022.CCSTUDIO.https://www.ti.com/tool/CCSTUDIO
[34]Texas Instruments.2022.Detection Layer Parameter TuningGuide for the 3D People Counting Demo.https://dev.ti.com/tirex/explore/node?node=AEdNr6XV-uJkInkTP0HOAw__VLyFKFf__LATEST
[35]Texas Instruments.2022.TI IWR6843.https://www.ti.com/product/IWR6843
[36]Babak Jamali,Deeban Ramalingam,and Aydin Babakhani.2020.Intelligent material classification and identification using a broadband millimeter-wave frequency comb receiver.IEEE Sensors Letters 4,7(2020),1–4.
[37]Chengkun Jiang,Junchen Guo,Yuan He,Meng Jin,Shuai Li,and Yunhao Liu.2020.MmVib:Micrometer-Level Vibration Measurement with Mmwave Radar.Association for Computing Machinery,New York,NY,USA.https://doi.org/10.1145/3372224.3419202
[38]Ozcan Kayikcioglu,Sinan Bilgin,Goktug Seymenoglu,and Artuner Deveci.2017.State and trait anxiety scores of patients receiving intravitreal injections.Biomedicine hub 2,2(2017),


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:31</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:31


[39]Zachary D.King,Judith Moskowitz,Begum Egilmez,Shibo Zhang,Lida Zhang,Michael Bass,John Rogers,Roozbeh Ghaffari,Laurie Wakschlag,and Nabil Alshurafa.2019.Micro-Stress EMA:A Passive Sensing Framework for Detecting in-the-Wild Stress in Pregnant Mothers.Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.3,3,Article 91(sep 2019),22pages.https://doi.org/10.1145/3351249
[40]Mika Kivimäki and Andrew Steptoe.2018.Effects of stress on the development and progression of cardiovascular disease.Nature Reviews Cardiology 15,4(2018),215–229.
[41]Takumi Kobayashi.2019.Large Margin In Softmax Cross-Entropy Loss..In BMVC.139.
[42]Rafal Kocielnik,Natalia Sidorova,Fabrizio Maria Maggi,Martin Ouwerkerk,and Joyce HDM Westerink.2013.Smart technologies for long-term stress monitoring at work.In proceedings of the 26th IEEE international symposium on computer-based medical systems.IEEE,53–58.
[43]PCF Law,LS Too,Peter Butterworth,K Witt,N Reavley,and AJ Milner.2020.A systematic review on the effect of work-related stressors on mental health of young workers.International Archives of Occupational and Environmental Health 93,5(2020),611–622.
[44]Garmin Ldt.2022.Venu Sq.https://www.garmin.com/en-AU/p/707174
[45]Garmin Ldt.2022.What Is the Stress Level Feature on My Garmin Device?https://support.garmin.com/en-US/?faq=WT9BmhjacO4ZpxbCc0EKn9
[46]Tianhong Li,Lijie Fan,Mingmin Zhao,Yingcheng Liu,and Dina Katabi.2019.Making the invisible visible:Action recognition through walls and occlusions.In Proceedings of the IEEE/CVF International Conference on Computer Vision.872–881.
[47]Ye Li,Antonia Krefeld-Schwalb,Daniel G.Wall,Eric J.Johnson,Olivier Toubia,and Daniel M.Bartels.0.The More You Ask,the Less You Get:When Additional Questions Hurt External Validity.Journal of Marketing Research 0,0(0),00222437211073581.https://doi.org/10.1177/00222437211073581arXiv:https://doi.org/10.1177/00222437211073581
[48]Zhengxiong Li,Fenglong Ma,Aditya Singh Rathore,Zhuolin Yang,Baicheng Chen,Lu Su,and Wenyao Xu.2020.WaveSpy:Remote and Through-wall Screen Attack via mmWave Sensing.In 2020IEEE Symposium on Security and Privacy (SP).217–232.https://doi.org/10.1109/SP40000.2020.00004
[49]Zhengxiong Li,Zhuolin Yang,Chen Song,Changzhi Li,Zhengyu Peng,and Wenyao Xu.2018.E-Eye:Hidden Electronics Recognition through MmWave Nonlinear Effects.In Proceedings of the 16th ACM Conference on Embedded Networked Sensor Systems (Shenzhen,China)(SenSys '18).Association for Computing Machinery,New York,NY,USA,68–81.https://doi.org/10.1145/3274783.3274833
[50]Yumeng Liang,Anfu Zhou,Huanhuan Zhang,Xinzhe Wen,and Huadong Ma.2021.FG-LiquID:A Contact-Less Fine-Grained Liquid Identifier by Pushing the Limits of Millimeter-Wave Sensing.Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.5,3,Article 116(sep 2021),27pages.https://doi.org/10.1145/3478075
[51]Bo Liu,Ying Wei,Yu Zhang,and Qiang Yang.2017.Deep Neural Networks for High Dimension,Low Sample Size Data..In IJCAI.2287–2293.
[52]Haipeng Liu,Yuheng Wang,Anfu Zhou,Hanyue He,Wei Wang,Kunpeng Wang,Peilin Pan,Yixuan Lu,Liang Liu,and Huadong Ma.2020.Real-Time Arm Gesture Recognition in Smart Home Scenarios via Millimeter Wave Sensing.Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.4,4,Article 140(dec 2020),28pages.https://doi.org/10.1145/3432235
[53]Jianyi Liu,Yansheng Qu,Jiaqi Li,Yunxiao Wang,Jing Zhang,and Hongshan Yin.2021.Malicious Code Family Classification Method Based on Spatial Pyramid Pooling and Deep Residual Network.In 2021IEEE 7th International Conference on Cloud Computing and Intelligent Systems (CCIS).260–264.https://doi.org/10.1109/CCIS53392.2021.9754597
[54]Yu Liu,Yuheng Wang,Haipeng Liu,Anfu Zhou,Jianhua Liu,and Ning Yang.2020.Long-Range Gesture Recognition Using Millimeter Wave Radar.In Green,Pervasive,and Cloud Computing:15th International Conference,GPC 2020,Xi'an,China,November 13–15,2020,Proceedings (Xi'an,China).Springer-Verlag,Berlin,Heidelberg,30–44.https://doi.org/10.1007/978-3-030-64243-3_3
[55]Ilya Loshchilov and Frank Hutter.2018.Fixing weight decay regularization in adam.(2018).
[56]Garmin Ltd.2022.STRESS TRACKING.garmin.com/en-US/garmin-technology/health-science/stress-tracking/
[57]Mahdi Boloursaz Mashhadi,Mikolaj Jankowski,Tze-Yang Tung,Szymon Kobus,and Deniz Gündüz.2021.Federated mmWave beam selection utilizing LIDAR data.IEEE Wireless Communications Letters 10,10(2021),2269–2273.
[58]Takemi Matsui and Satoshi Katayose.2014.A novel method to estimate changes in stress-induced salivary α-amylase using heart rate variability and respiratory rate,as measured in a non-contact manner using a single radar attached to the back of a chair.Journal of Medical Engineering &Technology 38,6(2014),302–306.
[59]Daniel J.McDuff,Javier Hernandez,Sarah Gontarek,and Rosalind W.Picard.2016.COGCAM:Contact-Free Measurement of Cognitive Stress During Computer Tasks with a Digital Camera.In Proceedings of the 2016CHI Conference on Human Factors in Computing Systems (San Jose,California,USA)(CHI '16).Association for Computing Machinery,New York,NY,USA,4000–4004.https://doi.org/10.1145/2858036.2858247
[60]Bruce S.McEwen and Eliot Stellar.1993.Stress and the Individual:Mechanisms Leading to Disease.Archives of Internal Medicine 153,18(091993),2093–2101.https://doi.org/10.1001/archinte.1993.00410180039004arXiv:https://jamanetwork.com/journals/jamainternalmedicine/articlepdf/617820/archinte_153_18_004.pdf
[61]Chintan Mehta,Ankit K Bhavsar,Hetal Oza,and Subhash Shah.2018.MySQL 8administrator's guide:effective guide to administering high-performance MySQL 8solutions.Packt Publishing


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>110:32•Liang et</header>


110:32•Liang et


[62]Zhen Meng,Song Fu,Jie Yan,Hongyuan Liang,Anfu Zhou,Shilin Zhu,Huadong Ma,Jianhua Liu,and Ning Yang.2020.Gait recognition for co-existing multiple people using millimeter wave sensing.In Proceedings of the AAAI Conference on Artificial Intelligence,Vol.34.849–856.
[63]Aditya Krishna Menon,Sadeep Jayasumana,Ankit Singh Rawat,Himanshu Jain,Andreas Veit,and Sanjiv Kumar.2020.Long-tail learning via logit adjustment.arXiv preprint arXiv:2007.07314(2020).
[64]Susan Michie.2002.Causes and management of stress at work.Occupational and environmental medicine 59,1(2002),67–72.
[65]K Mohanavelu,R Lamshe,S Poonguzhali,K Adalarasu,and M Jagannath.2017.Assessment of human fatigue during physical performance using physiological signals:a review.Biomedical and Pharmacology Journal 10,4(2017),1887–1896.
[66]Changiz Mohiyeddini and Stuart Semple.2013.Displacement behaviour regulates the experience of stress in men.Stress 16,2(2013),163–171.https://doi.org/10.3109/10253890.2012.707709arXiv:https://doi.org/10.3109/10253890.2012.707709
[67]Sandrine R Muller,Xi Leslie Chen,Heinrich Peters,Augustin Chaintreau,and Sandra C Matz.2021.Depression predictions from GPS-based mobility do not generalize well to large demographically heterogeneous samples.Scientific Reports 11,1(2021),1–10.
[68]Nermine Munla,Mohamad Khalil,Ahmad Shahin,and Azzam Mourad.2015.Driver stress level detection using HRV analysis.In 2015International Conference on Advances in Biomedical Engineering (ICABME).61–64.https://doi.org/10.1109/ICABME.2015.7323251
[69]Kai Niu,Fusang Zhang,Zhaoxin Chang,and Daqing Zhang.2018.A fresnel diffraction model based human respiration detection system using COTS Wi-Fi devices.In Proceedings of the 2018ACM International Joint Conference and 2018International Symposium on Pervasive and Ubiquitous Computing and Wearable Computers.416–419.
[70]Holly Ober.2022.Surveys with repetitive questions yield bad data,study finds.https://news.ucr.edu/articles/2022/01/28/surveys-repetitive-questions-yield-bad-data-study-finds
[71]Jung Ha Park,Ji Hyun Moon,Hyeon Ju Kim,Mi Hee Kong,and Yun Hwan Oh.2020.Sedentary lifestyle:overview of updated evidence of potential health risks.Korean journal of family medicine 41,6(2020),365.
[72]Selena R Pasadyn,Mohamad Soudan,Marc Gillinov,Penny Houghtaling,Dermot Phelan,Nicole Gillinov,Barbara Bittel,and Milind Y Desai.2019.Accuracy of commercially available heart rate monitors in athletes:a prospective study.Cardiovascular diagnosis and therapy 9,4(2019),379.
[73]Adam Paszke,Sam Gross,Francisco Massa,Adam Lerer,James Bradbury,Gregory Chanan,Trevor Killeen,Zeming Lin,Natalia Gimelshein,Luca Antiga,Alban Desmaison,Andreas Kopf,Edward Yang,Zachary DeVito,Martin Raison,Alykhan Tejani,Sasank Chilamkurthy,Benoit Steiner,Lu Fang,Junjie Bai,and Soumith Chintala.2019.PyTorch:An Imperative Style,High-Performance Deep Learning Library.In Advances in Neural Information Processing Systems 32.Curran Associates,Inc.,8024–8035.http://papers.neurips.cc/paper/9015-pytorch-an-imperative-style-high-performance-deep-learning-library.pdf
[74]Linda Gay Peterson and Lori Pbert.1992.Effectiveness of a meditation-based stress reduction program in the treatment of anxiety disorders.Am J Psychiatry 149,7(1992),936–943.
[75]Akarsh Prabhakara,Tao Jin,Arnav Das,Gantavya Bhatt,Lilly Kumari,Elahe Soltanaghaei,Jeff Bilmes,Swarun Kumar,and Anthony Rowe.2022.High Resolution Point Clouds from mmWave Radar.arXiv preprint arXiv:2206.09273(2022).
[76]Kun Qian,Zhaoyuan He,and Xinyu Zhang.2020.3D point cloud generation with millimeter-wave radar.Proceedings of the ACM on Interactive,Mobile,Wearable and Ubiquitous Technologies 4,4(2020),1–23.
[77]Yanghui Rao,Haoran Xie,Jun Li,Fengmei Jin,Fu Lee Wang,and Qing Li.2016.Social emotion classification of short text via topic-level maximum entropy model.Information &Management 53,8(2016),978–986.
[78]Rahat Jahangir Rony and Nova Ahmed.2019.Monitoring Driving Stress using HRV.In 201911th International Conference on Communication Systems Networks (COMSNETS).417–419.https://doi.org/10.1109/COMSNETS.2019.8711411
[79]Stanisław Saganowski,Przemysław Kazienko,Maciej Dziezyc,Patrycja Jakimów,Joanna Komoszynska,Weronika Michalska,Anna Dutkowiak,A Polak,Adam Dziadek,and Michal Ujma.2020.Review of consumer wearables in emotion,stress,meditation,sleep,and activity detection and analysis.arXiv preprint arXiv:2005.00093(2020).
[80]Hans Selye.2013.Stress in health and disease.Butterworth-Heinemann.
[81]Grant S Shields,Matthew A Sazma,and Andrew P Yonelinas.2016.The effects of acute stress on core executive functions:A meta-analysis and comparison with cortisol.Neuroscience &Biobehavioral Reviews 68(2016),651–668.
[82]Akash Deep Singh,Sandeep Singh Sandha,Luis Garcia,and Mani Srivastava.2019.Radhar:Human activity recognition from point clouds generated through a millimeter-wave radar.In Proceedings of the 3rd ACM Workshop on Millimeter-wave Networks and Sensing Systems.51–56.
[83]Youn-Sik Son,Hyuk-Kee Sung,and Seo Heo.2018.Automotive Frequency Modulated Continuous Wave Radar Interference Reduction Using Per-Vehicle Chirp Sequences.Sensors 18(082018),2831.https://doi.org/10.3390/s18092831
[84]P.Stoica,Zhisong Wang,and Jian Li.2002.Robust Capon beamforming.In Conference Record of the Thirty-Sixth Asilomar Conference on Signals,Systems and Computers,2002.,Vol.1.876–880vol.1.https://doi.org/10.1109/ACSSC.2002.1197303
[85]Gustavo E.Tafet and Renato Bernardini.2003.Psychoneuroendocrinological links between chronic stress and depression.Progress in Neuro-Psychopharmacology and Biological Psychiatry 27,6(2003),


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:33</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:33


[86]Sheng Tan,Yili Ren,Jie Yang,and Yingying Chen.2022.Commodity WiFi Sensing in Ten Years:Status,Challenges,and Opportunities.IEEE Internet of Things Journal 9,18(2022),17832–17843.
[87]Sheng Tan and Jie Yang.2016.WiFinger:Leveraging commodity WiFi for fine-grained finger gesture recognition.In Proceedings of the 17th ACM international symposium on mobile ad hoc networking and computing.201–210.
[88]Sheng Tan,Linghan Zhang,Zi Wang,and Jie Yang.2019.MultiTrack:Multi-User Tracking and Activity Recognition Using Commodity WiFi.In Proceedings of the 2019CHI Conference on Human Factors in Computing Systems (Glasgow,Scotland Uk)(CHI '19).Association for Computing Machinery,New York,NY,USA,1–12.https://doi.org/10.1145/3290605.3300766
[89]tauhidurrahman.2014.Montreal Imaging Stress Test Arithmetic.https://github.com/tauhidurrahman/YoutubeGUITutorial
[90]Alfonso Troisi.2002.Displacement Activities as a Behavioral Measure of Stress in Nonhuman Primates and Human Subjects.Stress 5,1(2002),47–54.https://doi.org/10.1080/102538902900012378arXiv:https://doi.org/10.1080/102538902900012378[91]Ashish Vaswani,Noam Shazeer,Niki Parmar,Jakob Uszkoreit,Llion Jones,Aidan N Gomez,Ł ukasz Kaiser,and Illia Polosukhin.2017.Attention is All you Need.In Advances in Neural Information Processing Systems,I.Guyon,U.Von Luxburg,S.Bengio,H.Wallach,
R.Fergus,S.Vishwanathan,and R.Garnett (Eds.),Vol.30.Curran Associates,Inc.https://proceedings.neurips.cc/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf
[92]Susanne Vernim and Gunther Reinhart.2016.Usage frequency and user-friendliness of mobile devices in assembly.Procedia CIRP 57(2016),510–515.[93]María Viqueira Villarejo,Begoña García Zapirain,and Amaia Méndez Zorrilla.2012.A Stress Sensor Based on Galvanic Skin Response (GSR)Controlled by ZigBee.Sensors 12,5(2012),6075–6101.https://doi.org/10.3390/s120506075
[94]Shweta Ware,Chaoqun Yue,Reynaldo Morillo,Jin Lu,Chao Shang,Jayesh Kamath,Athanasios Bamis,Jinbo Bi,Alexander Russell,and Bing Wang.2018.Large-Scale Automatic Depression Screening Using Meta-Data from WiFi Infrastructure.Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.2,4,Article 195(dec 2018),27pages.https://doi.org/10.1145/3287073
[95]Zhiqing Wei,Fengkai Zhang,Shuo Chang,Yangyang Liu,Huici Wu,and Zhiyong Feng.2022.MmWave Radar and Vision Fusion for Object Detection in Autonomous Driving:A Review.Sensors 22,7(2022),2542.
[96]Min Wu,Hong Cao,Hai-Long Nguyen,Karl Surmacz,and Caroline Hargrove.2015.Modeling perceived stress via HRV and accelerometer sensor streams.In 201537th Annual International Conference of the IEEE Engineering in Medicine and Biology Society (EMBC).1625–1628.https://doi.org/10.1109/EMBC.2015.7318686
[97]Yaxiong Xie,Zhenjiang Li,and Mo Li.2015.Precise power delay profiling with commodity WiFi.In Proceedings of the 21st Annual International Conference on Mobile Computing and Networking.53–64.
[98]Chenhan Xu,Huining Li,Zhengxiong Li,Hanbin Zhang,Aditya Singh Rathore,Xingyu Chen,Kun Wang,Ming-chun Huang,and Wenyao Xu.2021.CardiacWave:A MmWave-Based Scheme of Non-Contact and High-Definition Heart Activity Computing.Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.5,3,Article 135(sep 2021),26pages.https://doi.org/10.1145/3478127
[99]Yuzhe Yang,Hao Wang,and Dina Katabi.2022.On multi-domain long-tailed recognition,imbalanced domain generalization and beyond.In European Conference on Computer Vision.Springer,57–75.
[100]Sunghyun Yoon,Jai Kyoung Sim,and Young-Ho Cho.2016.A flexible and wearable human stress monitoring patch.Scientific reports 6,1(2016),1–11.
[101]Youwei Zeng,Dan Wu,Jie Xiong,Jinyi Liu,Zhaopeng Liu,and Daqing Zhang.2020.MultiSense:Enabling multi-person respiration sensing with commodity wifi.Proceedings of the ACM on Interactive,Mobile,Wearable and Ubiquitous Technologies 4,3(2020),1–29.
[102]Yong Zhou,Yanyan Dong,Fujin Hou,and Jianqing Wu.2022.Review on Millimeter-Wave Radar and Camera Fusion Technology.Sustainability 14,9(2022),


# A APPENDIX


While the previous studies [66,90]demonstrate the correlation between displacement activities and stress through physician observations,the goal of mmStress is to monitor human activity through mmWave radio and then infer stress levels autonomously.Here,we verify the correlation between human activity from "mmWave radio eyes"and stress,with the following feasibility study


Experiment Setup:We recruit ten volunteers,and eight of them return valid data.To acquire the ground-truth stress labels,we ask each volunteer to wear a Garmin watch simultaneously,which can generate a stress value every three minutes and classify stress into low,medium,and high levels (More details in


Meanwhile,we collect volunteers'activities using mmWave radar,in terms of movement trajectories and point clouds of the subject.We align these activity data with stress labels at the same period and compute 42statistics values from the sensed data,which can be divided into three categories:(i)Time.We decompose the timestamps corresponding to stress and activity into three features,days of the week,hours,and minutes.(ii)Trajectory.We


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>110:34•Liang et al.</header>


110:34•Liang et al.




Fig.25.The Pearson correlation coefficients between activity features and stress of all volunteers,where red represents a negative correlation between the feature and stress,blue represents a positive correlation.The darker the color the stronger the correlation.(p−value<0.05)


extract the trajectory within the time window (three minutes)as the number of data (N),the distance of the subject's movement (D),the max,min,mean and variance of the velocity in the x,y and z directions (vx_max,vx_min,vx_mean,vx_variance,vy_max, $v_{y}.$_min,vy_mean, $v_{y_{-}}$variance,vz_max,vz_min,vz_mean,vz_variance),and the max,min,mean and variance of the acceleration in the x and y directions (ax_max,ax_min,ax_mean,ax_variance, $a_{y}.$_max, $a_{y}.$_min, $a_{y}.$_mean, $a_{y_{-}}$variance)in the Cartesian coordinate.(iii)Point Cloud.We extract the point clouds within the time window (3minutes)as max,min,and mean of the number of point clouds (Np_max,Np_min,Np_mean),max,min,and mean of the point cloud positions in the x,y,and z directions (x_max,x_min,x_mean,y_max,y_min, $y_{*}$_mean,z_max,z_min,z_mean)in the Cartesian coordinate,and max,min,mean,and variance of the point cloud radial velocities (vr_max,vr_min,vr_mean,vr_variance).


We then compute ρ,the Pearson correlation coefficient to quantify the correlation between each feature and the stress,i.e.,


$$\rho=\frac{C o v\left(X,Y\right)}{\sigma_{X}\sigma_{Y}}.$$








X0


where Cov(X,Y)is the covariance of feature Xand stress Y,and $\sigma_{X}$and σYdenote the standard deviation of feature Xand stress value Y,respectively.In addition,we calculate the p−valueto evaluate the significance level of the extracted features with stress.We illustrate the relationship between stress and activity with the correlation coefficients among all volunteers as shown in Fig.25.


By calculating the correlation coefficients between time,human activity features,and stress,we found 3issues that could be studied in depth:


Activity intensity is highly correlated with stress.We depict the distribution of Pearson correlation coefficients between activity features and stress for all volunteers in Fig.26.We observe that (i)The top-3features with the highest correlation with stress are:the maximum value in the direction of the z-axis (z_max),the number of data (N),and the maximum number of point clouds (Np_max).Note that these features describe the intensity of human activity over time.The result indicates that for some people,the higher the stress,the higher the intensity and frequency of human activity,which corroborates our empirical feeling.(ii)Similarly,the minimum values in the activity features such as vx_minand vy_minare most negatively correlated with stress,which further demonstrates that some people under stress may reduce daily activities significantly.


High individual variation over stress features.From Fig 26,the std.,i.e.,the difference between the upper and lower edges of each box,implies high variation among individuals,in terms of the impact of the same feature.


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.</footer>
<header>mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:35</header>


mmStress:Distilling Human Stress from Daily Activities via Contact-less Millimeter-wave Sensing •110:35




Fig.26.Box plot of Pearson correlation coefficients of activity features and stress for all volunteers.(p−value<


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September</footer>
<header>110:36•Liang et al.</header>


110:36•Liang et al.


In addition,we can observe that there are always values scattered outside the box in each box plot,indicating that
there are always volunteers whose time and activity features correlate in a very different way.To quantify such variation,we calculate the coefficient of variation (CV)of the Pearson correlation coefficient between individual volunteer's activity features and stress levels using Equation 12:


$$\mathrm{C V}_{\rho}=\frac{\sigma_{\rho}}{\mu_{\rho}}$$





where $\sigma_{\rho}$indicates the standard deviation of the Pearson correlation coefficient across volunteers for the same characteristic and $\mu_{\rho}$indicates the mean value. $C V\geq0.\ vec{15}$indicates a large difference between the values of the group.We count the proportion of $C V\geq0.15$and $C V<0.15$for all features,with 65.9%of CV≥0.15and 34.1%of $C V<0.15$.It can be concluded that the majority (65.9%)of the correlations between activity features and stress differed significantly between individuals.Moreover,as in the specific example given in Fig.27,we compare the Pearson correlation coefficients of three activities with stress for three volunteers.It can be seen that for volunteers #3,#4,and #6,the point clouds have similar correlations for stress at the mean position on the z-axis (z_mean).As for the mean position of the point cloud on the x-axis in space (x_mean),only volunteer #3exhibits a relatively high correlation between this feature and stress.Unlike volunteers #4and #6,for the feature of the maximum number of point clouds (Np_max),only volunteer #3showed a lower correlation of this feature with stress.It inspires us to use personalized models in subsequent experiments to infer human stress levels using activity data.




$0.27$


$0.35$


Fig.27.The same activity feature has different impact on different people.The value in each cell represents the Pearson correlation coefficient between the feature in that row and stress at the column.


To sum up,our analysis positively confirms the correlation between human activity and stress,which indicates the feasibility of distilling stress from daily activities.On the other hand,the relationship varies significantly across different individuals,which leads to poor performance of traditional machine learning models with handcrafted features (like SVM or XGBoost,details in Sec.6.1.1).The findings motivate the design of mmStressNet,a custom-designed deep neural network to extract human activity features and classify stress autonomously in Sec.4.3.


Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.


<footer>Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Vol.7,No.3,Article 110.Publication date:September 2023.</footer>
