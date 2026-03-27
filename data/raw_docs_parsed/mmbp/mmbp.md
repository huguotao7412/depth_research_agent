<header>PDF Download 3560905.3568506.pdf 20January 2026
Total Citations:27Total Downloads:1273 ACM DIGITAL  1 Computing Machinery  Associatien for acmopen> LIBRARY CK10</header>


CK10


ACM DIGITAL  1 Computing Machinery  Associatien for acmopen> LIBRARY


Latest updates:


RESEARCH-ARTICLE


# mmBP:Contact-Free Millimetre-Wave Radar Based Approach to Blood Pressure Measurement


ZHENGUO SHI,Macquarie University,Sydney,NSW,Australia TAO GU,Macquarie University,Sydney,NSW,Australia YU ZHANG,Macquarie University,Sydney,NSW,Australia XI ZHANG,RMIT University,Melbourne,VIC,Australia


Open Access Support provided by:RMIT University Macquarie University


PDF Download 3560905.3568506.pdf 20January 2026
Total Citations:27Total Downloads:1273


Published:06November 2022


Citation in BibTeX format


SenSys '22:The 20th ACM Conference on
Embedded Networked Sensor Systems November 6-9,2022
Massachusetts,Boston


Conference Sponsors:SIGBED
SIGMOBILE SIGOPS
SIGARCH SIGMETRICS SIGCOMM


SenSys '22:Proceedings of the 20th ACM Conference on Embedded Networked Sensor Systems (November 2022)h ps://doi.org/10.1145/3560905.3568506ISBN:9781450398862


<footer>SenSys '22:Proceedings of the 20th ACM Conference on Embedded Networked Sensor Systems (November 2022)h ps://doi.org/10.1145/3560905.3568506ISBN:9781450398862</footer>
# mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measurement


Zhenguo Shi1,Tao Gu1,Yu Zhang1,Xi Zhang2
1School of Computing,Macquarie University,Australia
2School of computing technologies,RMIT University,Australia Email:


# ABSTRACT


Blood pressure (BP)measurement is an indispensable tool in diagnosing and treating many diseases such as cardiovascular failure and stroke.Traditional direct measurement can be invasive,and wearable-based methods may have limitations of discomfort and inconvenience.Contact-free BP measurement has been recently advocated as a promising alternative.In particular,Millimetre-wave (mmWave)sensing has demonstrated its promising potential,however it is confronted with several challenges including noise and vulnerability to human's tiny motions which may occur intentionally and inevitably.In this paper,we propose mmBP,a contact-free mmWave-based BP measurement system with high accuracy and motion robustness.Due to the high frequency and short wavelength,mmWave signals received in the time domain are dramatically susceptible to ambient noise,and deteriorating signal quality.To reduce noise,we propose a novel delay-Doppler domain feature transformation method to exploit mmWave signal's characteristics and features in the delay-Doppler domain to significantly improve signal quality for pulse waveform construction.We also propose a temporal referential functional link adaptive filter leveraging on the periodic and correlation characteristics of pulse waveform signals to alleviate the impact of human's tiny motions.Extensive experiment results achieved by the leave-one-out cross-validation (LOOCV)method demonstrate that mmBP achieves the mean errors of 0.87mmHg and 1.55mmHg for systolic blood pressure (SBP)and diastolic blood pressure (DBP),respectively;and the standard deviation errors of 5.01mmHg and 5.27mmHg for SBP and DBP,


# CCS CONCEPTS


•Human-centered computing →Ubiquitous and mobile computing systems and


# KEYWORDS


Blood pressure,contact-free sensing,mmWave


ACM Reference Format:


ACM Reference Format:Zhenguo Shi1,Tao Gu1,Yu Zhang1and Xi Zhang2.2022.mmBP:Contactfree Millimetre-wave Radar based Approach to Blood Pressure


Permission to make digital or hard copies of all or part of this work for personal or
classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page.Copyrights for components of this work owned by others than ACM must be honored.Abstracting with credit is permitted.To copy otherwise,or republish,to post on servers or to redistribute to lists,requires prior specific permission and/or a fee.Request permissions from permissions@acm.org.
SenSys '22,November 6–9,2022,Boston,MA,USA
©2022Association for Computing Machinery.
ACM ISBN


667


In ACM Conference on Embedded Networked Sensor Systems (SenSys '22),November 6–9,2022,Boston,MA,USA.ACM,New York,NY,USA,15


# 1INTRODUCTION


Blood pressure (BP),a periodic signal exerted by heartbeats,is one of the most representative physiological signs of human beings.BP is also a crucial indicator for physicians to diagnose cardiovascular conditions and treat related diseases [26,32].A human's blood pressure goes up and down between the maximum blood pressure,i.e.,systolic blood pressure (SBP),and the minimum pressure,i.e.,diastolic blood pressure (DBP),reflecting valuable information about health condition [3,65].BP measurement has become significantly important to our daily life,hence receiving particular interest from both academia and


Among a range of BP measurement methods developed over decades,the "gold standard"is direct BP measurement using particular medical devices placed into the arterial line of subject [35,56].Although it achieves high accuracy,this method is invasive,causing pain or risk of infection [36].Non-invasive BP measurement has been advocated as a safe and convenient alternative,hence attracting increasing attention.In such a context,BP measurement can be accomplished by exploiting the property of physiological characteristics.In particular,pulse wave has been widely used for BP measurement as it essentially contains adequate BP-related features,e.g.,peak value,minimum value,and first inflection [4].With pulse waveform analysis techniques,these features can be processed to build an effective relationship between pulse waveform and BP values,achieving successful BP measurements.Towards this end,several BP measurement methods have been proposed to capture pulse-related physiological signals,e.g.,Photoplethysmography (PPG)[10,50],using dedicated devices such as wrist-watch or finger/arm cuff.Despite promising,these contact-based BP measurements have some shortcomings.First,their performance is highly dependent on subject's physical movements,ambient lighting conditions or even skin tattoos.Second,users may feel uncomfortable when carrying devices or even painful due to cuff inflation


Contact-free BP measurement has been proposed recently leveraging on camera or wireless sensor [9,29].The camera-based BP measurement utilizes the property of video/image data induced by pulse motions such as the pulse motions at fingertip [60].However,its performance relies heavily on illumination conditions and motion changes.A small change in light or movement may degrade accuracy dramatically.Wireless sensor-based methods leverage on radio frequency signals to acquire skin or blood vessel displacement caused by pulse wave transmission for BP measurement [6].Despite the progress achieved,these systems may not achieve accurate measurement as they cannot accurately capture tiny skin or vessel


<footer>Permission to make digital or hard copies of all or part of this work for personal or
classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page.Copyrights for components of this work owned by others than ACM must be honored.Abstracting with credit is permitted.To copy otherwise,or republish,to post on servers or to redistribute to lists,requires prior specific permission and/or a fee.Request permissions from permissions@acm.org.
SenSys '22,November 6–9,2022,Boston,MA,USA
©2022Association for Computing Machinery.
ACM ISBN 667</footer>
<header>SenSys '22,November 6–9,2022,Boston,MA,USA Z.Shi,T.Gu,Y.Zhang and X.Zhang</header>


SenSys '22,November 6–9,2022,Boston,MA,USA


perturbations (i.e.,less than 1mm)due to low operating frequency and limited bandwidth


Millimetre-wave (mmWave)sensing has been advocated as a plausible solution for contact-free BP measurement.The high frequency and large bandwidth of mmWave enable capturing tiny variations caused by pulse activities [24,25,34,49].In particular,with mmWave signal reflection received at the receiver side,one can obtain the skin displacement.Since skin displacement is caused by pulse motions,the characteristics of pulse movements can be effectively captured and used for BP measurement [49].However,applying mmWave sensing for contact-free BP measurement is not a trivial task and several fundamental challenges remain to be addressed,which we summarize as


Challenge 1:Reconstructing high-quality pulse waveform from raw mmWave signals in the time domain is challenging.In such a context,raw mmWave signals received from mmWave radar are used to reflect the skin displacements caused by pulse wave activities.Due to their high frequency and short wavelength,mmWave signals in the time domain are highly sensitive to noise [59].As a result,mmWave reflections received are usually buried under the noise floor,i.e.,interference and background noise from the environment [51].The signal characteristics may be distorted,making it difficult to extract effective pulse-related features.Our preliminary study in Section 2.1shows that mmWave reflections received are largely contaminated by noise.In this situation,it is extremely hard to extract useful features from these signals for BP measurement,leading to poor performance.Therefore,noise reduction is a critical issue in mmWave-based BP


Many efforts have been devoted to noise reduction by leveraging signal characteristics in the time domain or the frequency domain.The matrix factorization is a time-domain based method commonly applied for noise reduction,e.g.,Non-Negative Matrix Factorization (NMF)[33,62].The fundamental is to isolate clean signals from noise by utilizing the property of the signal matrix.However,their implementation is highly complex,and involves a slow convergence process.Other time-domain based methods use principal component analysis (PCA)[66,67].They typically choose a certain group of principal components for signal reconstruction and noise reduction,however,selecting appropriate principal components can be challenging.Apart from that,signal characteristics in the frequency domain have also been investigated for noise reduction such as the Butterworth filter.The key idea is to filter out unwanted signals based on signal characteristics in the frequency domain [1,40].Although this filter is easy to implement and reduces noise partially,its performance is not satisfactory due to its fixed cut-off frequencies.Our preliminary study in Section 2.1demonstrates that these methods can improve pulse waveform patterns partially,but the outcomes are insufficient to construct accurate pulse signals.It is difficult to extract useful features from noise-contaminated signals in the time or frequency domain for successful BP


In this paper,we investigate novel features extracted from the delay-Doppler (DD)domain to address the aforementioned challenge.The fundamental idea is to exploit the delays (due to signal transmission time and distance)and Doppler shifts (due to target movement)in mmWave reflections for noise reduction.Since mmWave reflections caused by pulse movements and noise have


668


Z.Shi,T.Gu,Y.Zhang and X.Zhang


different responses in terms of transmission time,distance or movement speed,their delays and Doppler shifts can be considerably different.It will then be feasible to separate the clean mmWave reflections and noise using their corresponding properties in the DD domain.Note that,some techniques,such as the range-Doppler map,represent the distance-speed characteristics of objects,while it does not consider signal property in the time domain that however is an essential factor for pulse waveform construction.Based on the aforementioned,DD domain signal representation involves not only distance-speed properties but also signal variations in the time dimension.As a result,DD domain representation is able to construct pulse waveforms more comprehensively.Therefore,in this work,we transfer raw mmWave signals from the time domain to the DD domain and then separate the clean mmWave reflections with noise to significantly improve signal


Challenge 2:Traditional mmWave-based methods are susceptible to body motions due to the high operating frequency of mmWave signals.A subject is usually required to keep stationary to avoid large-scale motions during measurement,however,small-scale or tiny motions (e.g.,essential tremor and resting tremor)often occur unintentionally [2,15].Specifically,essential tremor is a fairly common disorder,which often presents with hand postures [2].Resting tremor usually occurs when keeping limb stationary or relaxed [37].Notably,tremor is more prevalent for elderly people,due to aging or some chronic diseases such as Parkinson's disease


It is worth noting that even though these tremors result in only small distance variations between mmWave radar and subject,they induce considerable influence on the performance of contact-free mmWave BP measurement.Specifically,a tiny motion will interact nonlinearly with the desired signal,leading to severe nonlinear distortion on signal property.For instance,for a mmWave signal operating at 75GHz,a less than 1mm change in distance may result in a πdistortion in phase information,corrupting the fundamental characteristics of pulse-related signals [23].Our preliminary study in Section 2.2shows that even though a normal 61years old adult keeps stationary,tiny motion occurs,leading to a considerable negative impact on mmWave signals.Consequently,we cannot extract proper features,resulting in pulse waveform construction


To tackle this challenge,numerous efforts have been made to investigate the motion-reduction problem.Signal decomposition algorithms (e.g.,Wavelet [45],Empirical Mode Decomposition (EMD)[46]and independent component analysis (ICA)[31])have been proposed to effectively decompose the received signal into several sub-components,with the purpose of separating the interference caused by motions and the clean signals.However,selecting appropriate decomposition parameters can be extremely challenging to ensure performance.Moreover,decomposition can only reduce motion to a certain degree,and the residual motion will still have a negative influence on the clean signals [63].Deep learning (DL)techniques (e.g.,deep contrastive learning and variational encoderdecoder network [11,69])have recently been proposed to mitigate motion impact.However,these techniques typically require large training samples and frequent re-training which limit their potential for real-world deployment.Apart from the above,nonlinear adaptive filter (NLAF)has the capability to address nonlinear motion and has demonstrated its effectiveness in speech signal processing


<footer>668</footer>
<header>mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measu SenSys '22,November 6–9,2022,Boston,MA,USA</header>


mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measu




Figure 1:Preliminary results –raw mmWave reflections processed by different noise reduction methods


[38].However,NLAF may not be directly applied in mmWavebased BP measurement as it requires the actual pulse waveform as a reference signal which is not available due to the lack of prior knowledge of noise or pulse signals.An attempt [28]has been made to produce a reference signal by using the delayed information of received data,however,the performance of motion reduction is not satisfactory due to the high correlation between artificial signal and raw pulse data [39].Therefore,despite promising,mitigating the impact of tiny motion on pulse construction using NLAF in mmWave-based BP measurement is still an open research problem.To tackle this problem,we propose a novel method to generate an effective reference signal and exploit the property of NLAF for BP measurement.The fundamental idea is that pulse morphology is a type of periodical repeat with high correlations over the time period.Even though each repeat may vary slightly over time,the overall pattern is stable.However,the tendency and the correlation property may no longer hold when tiny motions occur.This gives us an opportunity to generate a reference signal which is highly correlated with the clean pulse waveform but uncorrelated with the interference induced by tiny motions.With this reference signal,NLAF can be used to effectively reduce the impact of tiny motion on pulse waveform


Our Approach:To address the aforementioned challenges,in this paper we propose mmBP,a contact-free mmWave-based system for safe,high-accurate and motion-robust BP measurement.mmBP performs in the following three steps.First,use an off-the-shelf mmWave radar (i.e.,Texas Instruments,TI IWR1843BOOST)to capture the variations of mmWave reflections caused by pulse activities.Next,we transfer the mmWave signals received from the time domain to the DD domain,then extract the representative DD-domain pulse-related information and filter out noise based on the fact that noise and pulse signals have different properties in the DD domain.In the third step,we propose a novel motion


669


SenSys '22,November 6–9,2022,Boston,MA,USA


compensation scheme to address the influence of tiny motion on BP measurement leveraging on the property of NLAF.As aforementioned,NLAF cannot be directly applied to mmWave-based BP measurement due to the lack of reference signal.To solve this issue,we propose a novel method to generate an effective reference signal for NLAF,then apply compensation to reduce the impact of tiny motions.We perform extensive experiments to validate the effectiveness of mmBP with the dataset collected from 25normal subjects (11females and 14males),aged from 23to 61years old.Our major contributions are summarized as


•We propose a novel BP measurement system leveraging on
mmWave signal characteristics and representative features in the DD domain.mmBP is fully contact-free and does not require wearing any devices.mmBP is capable of achieving high accuracy and being robust to tiny motions,hence it is promising for potential real-world deployment.
•We propose a novel delay-Doppler domain feature transformation (DDFT)to extract representative features from the DD domain for pulse waveform construction,compared to the time domain or the frequency domain as commonly used in existing measurement methods.To the best of our knowledge,this is the first to leverage DD domain features to estimate BP values.DDFT is able to enhance the quality of pulse waveform and reduce noise influence.
•We propose a temporal referential functional link adaptive filter (TR-FLAF)to alleviate the impact of tiny motion on pulse waveform construction.For reliable filtering performance,we propose the temporal reference signal extraction (TRSE)algorithm to generate the reference signal for nonlinear adaptive filter by exploiting the periodic property and correlation character of the pulse signals.We then apply compensation to reduce the impact of motion on pulse information extraction,thereby improving the performance of BP measurement.
•We conduct extensive experiments to evaluate the performance of mmBP under various scenarios and settings.Results show that mmBP achieves the mean errors of 0.87mmHg and 1.55mmHg for SBP and DBP,respectively;and the standard deviation errors of 5.01mmHg and 5.27mmHg for SBP and DBP,


# 2PRELIMINARY STUDY


To investigate the feasibility of mmWave sensing in contact-free BP measurement,in this section,we conduct a preliminary study using an off-the-shelf mmWave radar (TI IWR1843BOOST).Table 1shows the device configuration in


# 2.1mmWave reflections in the time or frequency domain


In this study,we ask a subject (36years old male adult)to sit on a chair and place his hand and wrist on a desk.We place a mmWave radar on the desk,5cm above the subject's wrist.The subject is required to keep stationary during data collection.The mmWave radar emits Frequency-Modulated Continuous-Wave (FMCW)signals and receives the mmWave signals reflected from the skin.The signal variations capturing subtle skin displacements caused


<footer>669</footer>
<header>SenSys '22,November 6–9,2022,Boston,MA,USA Z.Shi,T.Gu,Y.Zhang and X.Zhang</header>


SenSys '22,November 6–9,2022,Boston,MA,USA




Figure 2:Preliminary results –raw mmWave signals with tiny motion processed by motion reduction methods


by pulse activities can be obtained by extracting pulse waveform features from mmWave signal reflections to achieve BP measurement.Fig.1(a)depicts raw mmWave reflections received in the time domain.We observe that these mmWave signals are largely contaminated by noise,i.e.,they are buried into noise.In this regard,it is difficult to extract proper features for successful BP measurement.Therefore,suppressing and reducing noise is a critical task in mmWave-based BP measurement.Much research efforts have been made for noise reduction from the time and frequency domains such as Butterworth (BW)filter [1],PCA [67],and NMF [62].Fig.1(b)to Fig.1(d)show the mmWave reflections processed by PCA,BW filter and NMF-based methods,respectively.As can be observed,for each noise reduction method,the waveform pattern is improved and presents some periodic features compared to raw time-domain signals.However,these periodic variations present coarse information about pulse motions,which is insufficient for accurate pulse waveform construction.Hence,using noise-contaminated timeor frequency-domain features may not be possible to achieve reliable BP


# 2.2mmWave reflections with tiny motions


Human's tiny motions may occur unintentionally and inevitably induce severe influence on mmWave signals.This may result in poor pulse waveform construction,dramatically degrading performance.In Fig.2(a),we demonstrate the impact of tiny motions on mmWave signals.In this figure,a subject (61years old female adult)is asked to keep stationary to avoid movements,and measure the raw mmWave reflections received from the same mmWave radar.It is obvious that tiny motion still occurs and causes dramatic nonlinear influence on mmWave reflections.This makes it impossible to extract effective features from mmWave signals for proper pulse waveform construction.Therefore,reducing the impact of tiny motions is of importance to successful BP


Motion reduction has attracted particular research attention in recent years.Several methods have been proposed,e.g.,ICA


670


Z.Shi,T.Gu,Y.Zhang and X.Zhang




Figure 3:Key processing steps in mmBP


[31],EMD [46]and NLAF [28],to reduce the impact of motions for clean signals.Fig.2(b)-Fig.2(d)depict the mmWave signals (with tiny motions)processed by ICA [31],EMD [46]and NLAF [28],respectively.As can be observed,for each method,the signal pattern is improved to a certain degree,implying that the impact of tiny motion is reduced.However,processed signals are still largely contaminated by tiny motions,making it impossible to construct accurate pulse waveforms.Therefore,reducing the impact of tiny motions on mmWave signals plays an essential role in reliable BP


# 3DESIGN OF MMBP


In this section,we present our design of mmBP.As depicted in Fig.3,mmBP measures BP values via the following four steps:mmWave Reflection Capturing,DD Domain Feature Transformation (DDFT),Motion Compensation,and BP Estimation.We first present an overview of mmBP,then describe each step in


mmWave Reflection Capturing:The first step captures the arterial pulse signal based on received mmWave reflections.Due to the high frequency and large bandwidth,mmWave signal can effectively reflect skin displacement caused by pulse motions,which is essential for pulse waveform construction.Since pulse signal (e.g.,waveform)contains adequate BP-related information,it can be processed to measure BP values and track their


DD Domain Feature Transformation:This step transforms the pulse signal obtained in the former step from the time domain to the DD domain for noise reduction.Since the desire pulse signals and noise have different delay and Doppler responses,it is possible to retain the desired signals and reduce noise influence in the DD domain,thereby enhancing pulse waveform


Motion Compensation:This step removes the impact of tiny motions on pulse waveform construction.To achieve this,we propose a temporal referential functional link adaptive filter (TR-FLAF)to mitigate nonlinear influence induced by tiny motions.In particular,we propose a temporal reference signal extraction (TRSE)algorithm to generate the reference signal for the adaptive filter,hence achieving reliable filtering


<footer>670</footer>
<header>mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measu SenSys '22,November 6–9,2022,Boston,MA,USA</header>


mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measu


BP Estimation:The final step first extracts six distinguishable DD features from the pulse waveform,which represent unique properties of BP activities.Then,we feed these features into a regression model to find the effective relationship between the extracted features and BP values,achieving a successful BP measurement.


# 3.1mmWave Reflection Capturing


In the first step,we extract pulse information from mmWave signal reflections.We use a commercial-grade mmWave radar,i.e.,TI IWR1843BOOST.The device transmits FMCW signals toward a subject's wrist and receives reflected signals.The pulse waveform can then be extracted from signal reflections.Let $x(t)$stand for the transmitted FMCW signal,which is


$$x(t)=A_{T}e^{j(2\pi f_{c}t+\pi\frac{B}{T}t^{2})},$$





where ATis the amplitude of the transmitted FMCW signal,fcstands for the central frequency,Bdenotes the system bandwidth,and Trepresents the chirp period.The received signal can be then obtained by


$$y(t)=A_{R}e^{j\left(2\pi f_{c}\left(t-t_{d}\right)+\pi\frac{B}{T}\left(t-t_{d}\right)^{2}\right)},$$





where tdis the delay between the transmitted signal and the received signal,and ARstands for the amplitude of the received signal.The value of ARis determined by not only the reflected energy of the skin surface but also the distance between the mmWave radar and the skin surface of the subject's wrist.The beat signal s(t),which contains the pulse information,can be obtained by mixing x(t)and y(t)as follows.


$$\begin{aligned}{}&{{}s(t)=x(t)y(t)\approx A(t)e^{j\left(2\pi f_{d}(t)t+\phi(t)\right)},}\\ {}&{{}A(t)=A_{T}A_{R},\quad f_{d}(t)=\frac{2B d(t)}{c T},\quad\phi(t)=\frac{4\pi d(t)}{\lambda},}\\ \end{aligned}$$





where A(t),fd(t)and $\phi(t)$denote the amplitude,frequency and phase of the beat signal,respectively.d(t)is the distance between the mmWave radar and the skin surface of wrist.crepresents the speed of light.λis the wavelength of mmWave signal.


The pulse variation will result in the displacement of the skin surface,leading to changes ofd(t).It is noteworthy that although all components of s(t)(i.e.,A(t),fd(t)and φ(t))can be used to extract the pulse waveform,phase information φ(t)is more suitable for small-scale vibration detection [34].Thus,in this paper,we treat φ(t)as the original source signal to extract pulse features for BP measurement.


# 3.2Delay-Doppler Domain Feature Transformation


Although phase signal φ(t)can reflect the skin displacement caused by pulse movements,it is extremely challenging to utilize φ(t)directly for BP measurement.This is because phase signal φ(t)obtained is usually contaminated by noise from environment.This will result in a low signal-to-noise ratio (SNR),implying that pulse waveform is overwhelmed by noise.Some signal processing techniques (e.g.,filter and signal decomposition)[33,62,66,67]can partially improve the quality of time-domain phase signal,but the improvement may not be sufficient for constructing a fine-grained pulse waveform.


671


SenSys '22,November 6–9,2022,Boston,MA,USA


Recall in Fig.1(a),there is no clear variation pattern in the original time-domain phase signal.Thus,it is very hard to extract pulse waveform using the time-domain data alone.Fig.1(b)to Fig.1(d)show the phase signals processed by PCA,BW filter and NMF-based methods,respectively.It is clear that all these three methods can improve the quality of phase signals to a certain degree,and periodic variations in the frequency domain can be captured which are related to pulse signals.However,these variations are too coarse to effectively reflect the essential features of pulse motions.Consequently,it is very difficult to construct a complete pulse waveform using time-domain signals.


To overcome the above challenge,we propose DDFT to extract effective features and construct pulse signals for effective BP measurement.Unlike existing methods that use time-domain phase signals for BP measurement,DDFT extracts distinguishable features from the DD domain.The key idea is that,on the one hand,the pulse signals are concentrated on certain resource grids in the DD domain.On the other hand,noise signals are mainly distributed in other resource grids due to their different DD properties from the pulse signals.In this regard,it is easy to separate pulse information and the interfering data,bringing two major attractive advantages.First,the variation of pulse signal is significantly enhanced,which is beneficial for fine-grained pulse representation.Second,noise can be considerably alleviated,resulting in a higher SNR.


Let ζstand for the phase noise in the time-domain,which is modelled as an additive white Gaussian noise (AWGN)with zero mean and variance σ2ζ.Thus,the received phase signal φ(t)can be expressed as


$$\phi(t)=\phi_{p}(t)+\zeta(t),$$





where φp(t)denotes the actual phase signal.Let Psbe the power of φp,then SNR in the time-domain is defined as $\mathrm{S N R}_{T}=\frac{P_{s}}{\sigma_{\zeta}^{2}}$.


$\phi_{p}(t)$


$\operatorname{o f}\phi_{P}$


Given the above time-domain signals,the DD domain pulse data can be extracted via the following two steps.First,we perform the Wigner transform operation to map φ(t)from the time domain to the time-frequency (TF)domain,which can be expressed as


$$R[n,m]=\int g^{*}\big(t-n T\big)\phi\big(t\ e^{-j2\pi m\Delta f\big t-n T\big)}d t,$$





where $g\left(t-n T\right)e^{-j2\pi m\Delta f\left(t-n T\right)}$stands for the receiving filter which aims to sample R[n,m]from φ(t). n∈$\{0,\ldots,N-1\}$and $\iota\\in\\{0,\ldots,M-1\}$denote time and frequency indices,respectively.


In the next step, $\bar{R}\left[n,m\right]$is converted into the DD domain signal,r[k,l],using symplectic finite Fourier transform (SFFT)[20],which is


$$\Lambda\left[k,l\right]=\frac{1}{\sqrt{N M}}\sum_{n=0}^{N-1}\sum_{m=0}^{M-1}R\left[n,m\right]e^{-j2\pi\left(\frac{k n}{N}-\frac{l m}{M}\right)},$$





wherek$\in\{0,\ldots,K-1\}$ and$\in\{0,\ldots,L-1\}$stand for Doppler and delay indices,respectively.Fig.4illustrates the phase representation in the DD domain processed by DDFT,from which it is obvious that the variation pattern (in the right subfigure)is significantly clearer and closer to pulse waveform,compared to signals illustrated in Fig.1(a)-Fig.1(d).In other words,a better pulse waveform can be constructed using the output from DDFT,due to the following reason.As can be observed,pulse signals are distributed in a certain


<footer>671</footer>
<header>Z.Shi,T.Gu,Y.Zhang and X.Zhang SenSys '22,November 6–9,2022,Boston,MA,USA</header>


SenSys '22,November 6–9,2022,Boston,MA,USA




Figure 4:Pulse morphology in the DD domain processed by DDFT


area in the DD domain because of its unique delay and Doppler properties.Consequently,the power of pulse signals mainly focuses on that area.On the other hand,noise signals distribute all grids in the DD domain.Under this situation,we select the row of Λ whose Doppler shift matches that of the pulse waveform and use it as DD-domain feature signal for further processing.Let rdenote the selected DD-domain feature signal,which can be expressed as r=�
$r\;=\;\widehat{\phi_{p}}+\widehat{\zeta_{i}}$where
$\widehat{\phi_{P}}$ stands for the selected phase signal in
DD-domain and its power �Psis approximate to Ps.�ζrepresents the noise of the selected row,which follows the AWGN distribution with zero mean and variance $\widetilde{\sigma_{\zeta}}^{2}$.In this regard,SNR of the selected
row is defined as SNRDD=�Ps�
$=\frac{\widehat{P_{s}}}{\widehat{\sigma_{\zeta}}^{2}}$.Since
$\widehat{\sigma_{\zeta}}^{2}$is much smaller than σ2
ζ
and �Psis close to Ps,SNRDDis much larger than SNRT=Ps
σ2
ζ
.This
can effectively reduce the impact of noise and other interference on pulse waveform construction as well as reduce complexity.


$=\frac{P_{s}}{\sigma_{\zeta}^{2}}$


$\widehat{P}_{s}$


# 3.3Motion Compensation


In reality,the performance of BP measurement may be vulnerable to subject's tiny motions such as unconscious finger or hand trembles.These tiny motions may occur inevitably,especially for the elderly or people with chronic diseases.Tiny movements induce nonlinear interference to pulse signals in the DD domain,as shown in Fig.5.As a result,it is impossible to construct a reliable pulse waveform using these contaminated DD-domain signals,leading to failure in BP measurement.Therefore,it is vital to address the impact of tiny motions on DD-domain signals for successful BP measurement.


Traditional motion reduction methods such as linear filters may not perform well as expected.This is because they concentrate on cancellation of linear noise,while the noise of tiny motions is nonlinear.Apart from that,nonlinear adaptive filter may potentially clean contaminated signals and has demonstrated its effectiveness in speech signal processing [17].However,it is hard to apply nonlinear adaptive filter directly to this work as it requires prior information (i.e.,reference signal)which is inaccessible for mmWave-based BP measurement due to no prior knowledge about noise or the desired signals.One way to achieve the reference signal is to minus the received signal from the corresponding delay data,but the quality of the output signal (i.e.,reference signal)is not sufficient to achieve reliable filtering performance.


672


Z.Shi,T.Gu,Y.Zhang and X.Zhang




Figure 5:Pulse morphology in the DD domain with tiny motions




Figure 6:Structure of TR-FLAF for motion compensation


In this section,we present a temporal referential functional link adaptive filter (TR-FLAF)to filter out the nonlinear impact caused by tiny motions to enhance the desired signal and construct an accurate pulse waveform.Note that,the performance of traditional FLAF is heavily dependent on the reference signal,which is not available for our work.To address this issue,we propose a temporal reference signal extraction (TRSE)algorithm to generate reference signals.This algorithm essentially searches and extracts uncontaminated signals from mmWave reflections by leveraging the periodic and correlated properties of pulse movements.Then,the extracted data can be treated as the reference signal.


The structure of TR-FLAF is demonstrated in Fig.6,TR-FLAF operates in three major steps:1)temporal reference signal c is generated based on the pulse representation in DD domain r(n);2)functional expansion of c generates Lsamples of expanded input v(n);and 3)the output of adaptive filter,g(n),is produced.To achieve estimated value,r(n),the coefficient of the filter is updated adaptively by utilizing error signal e(n).


3.3.1Temporal Reference Signal Extraction.This step generates temporal reference signals for the nonlinear adaptive filter.As demonstrated in Fig.5,the pulse morphology without motion is composed of periodical repeats within the time period.Even though each repeat changes slightly over time,the overall tendency is stable.By contrast,the pulse morphology becomes patternless when tiny motions occur.Moreover,we provide a heatmap of the correlation matrix ofr(n)to further analyze the impact of tiny motions on pulse movements,as illustrated in Fig.7.The color change from blue to


<footer>672</footer>
<header>SenSys '22,November 6–9,2022,Boston,MA,USA mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measu</header>


mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measu




Figure 7:Heatmap of correlation matrix Γ Figure 8:Performance of TR-
FLAF


yellow denotes that the correlation turns from low to high.In this figure,segments A and B correspond to the cases without and with tiny motions,respectively.It is obvious that segment A has higher correlation values with other segments compared to segment B.This is because segments for the case without tiny motions share similar patterns,thereby having high correlation values.On the contrary,segment B is contaminated by tiny motions,destroying the correlation characteristic with other segments.Therefore,we can determine the reference signal for TR-FLAF,drawing support from the correlation values of segments.


To achieve this,DD-domain feature signal ris divided into Isegments c1,...,cI.Iis calculated by two critical factors:the segment length and the overlapping region between adjacent segments.The segment length is set such that the duration is larger than one pulse period but less than two pulse periods.This can guarantee that each segment captures the overall property of pulse morphology with reduced complexity.The overlapping region enables the information to be shared between segments.Consequently,the impact of Ion BP measurement performance depends on the joint impact of segment length and overlapping region.In this paper,the values of segment length and overlapping region are empirically set to 500ms and 100ms,respectively.


Then the correlation matrix can be obtained by


$$\Gamma(i,j)=\operatorname{c o r}(c_{i},c_{j}),$$





where cor(.)stands for the correlation operation.For the ith row of Γ,α(i)is calculated which is the number of elements higher than a threshold.Note that,the threshold is specific to system configuration,i.e.,the segment length and the overlapping region between adjacent segments.So,its value does not change with different subjects.In this paper,the threshold is empirically set to 0.86.Then,the index with the largest value of αcan be achieved by


$$I_{m a x}=\operatorname{a r g}\operatorname*{m a x}_{i\in\left[1,I\right]}\ (\alpha(i)).$$





Consequen$\mathrm{t l y},\ c_{I_{m a x}}$ is selected as the reference signal.Note that,since instant pulse representations are different from time to time,the values of $I_{m a x}$and $c_{I_{m a x}}$vary over time.In this regard, $c_{I_{m a x}}$has to be calculated temporally for each BP measurement.For simplicity,cwill be used to indicate $c_{I_{m a x}}$for the rest of this paper.


3.3.2Functional Expansion Block.The objective of functional expansion block (FEB)is to enhance the quality of input $s i\mathrm n n a,$and FEB is composed of several functions obeying the universal approximation constraints [14].A variety of expansion models can be


673


SenSys '22,November 6–9,2022,Boston,MA,USA


employed including tensor,power series expansion and trigonometry expansion.In this paper,we use trigonometric expansion due to its computational efficiency and the concise representation of nonlinear functions [44].


For the nth iteration,the input vector c contains Kinput samples cand can be written as


$$\mathbf{c}=\big[c\big(n\big),c\big(n-1\big),\ldots,c\big(n-K+1\big)\big]^{T},$$


where cis the reference signal obtained in Section 3.3.1.





Given the above equation,we can obtain expanded input v(n)with Lelements based on trigonometric function expansion.Each element $\operatorname{o f}\mathbf{v}(n)$corresponds to input sample c(n),which can be expressed as


$$v_{j}(c(n))=\left\{\begin{array}{l l}{c(n),}&{\quad j=0}\\ {\operatorname{s i n}(q\pi c(n)),}&{\quad j=2q-1}\\ {\operatorname{c o s}(q\pi c(n),}&{\quad j=2q}\\ \end{array}\right.$$





where $q=1,2,\ldots,Q$ depicts the expansion index,and Qstands for the expansion order$j=0,1,\ldots,L-1$stands for the functional link index.


3.3.3Coefficient Adaptation.Upon obtaining v(n),the next step is to find out the coefficients of TR-FLAF,w,which is defined as


$$\mathbf{w}(n)=\big[w_{0}(n),w_{1}(n),\ldots,w_{L-1}(n)\big]^{T}.$$





The approximation of the nonlinear model can be achieved by minimizing error signal,e(n),given by


$$e(n)=r(n)-g(n)=r\big(n)-\mathbf{w}^{T}(n)\mathbf{v}(n).$$





To achieve a proper coefficient vector w,one possible way is to apply adaptive methods satisfying the gradient descent rule [52].In this paper,we use the adaptive method obeying the stochastic gradient rule to adjust the filter coefficients.The weight is updated as


$$\mathbf{w}\big(n+1\big)=\mathbf{w}\big(n\big)+\frac{\eta\mathbf{v}\big(n\big)}{\mathbf{v}^{T}(n)\mathbf{w}\big(n\big})$$


where ηis the step size.





Fig.8shows the pulse representation processed by TR-FLAF.We observe from this figure that the impact of tiny motion on pulse waveform is significantly reduced.The variation pattern of pulse morphology is considerably clearer,compared to that of contaminated signal with red color.Therefore,the quality of pulse signals is enhanced,contributing to reliable BP measurement.


# 3.4Blood Pressure Estimation


In this step,we extract six representative features from the pulse waveform in the DD domain.Then,we feed these DD domain features into the regression model for accurate BP measurement.


3.4.1DD domain feature extraction.A complete list of extracted


features in the DD domain are shown as follows.


Maximum peak (MP):MP is the highest point of a pulse waveform


in the DD domain,which corresponds to SBP.


First inflection point (FIP):FIP is the first inflection point of a pulse signal in the DD domain,which is related to DBP.


Maximum to minimum ratio (MMR):MMR is measured as the ratio of the maximum to minimum signal values of a pulse


<footer>673</footer>
<header>SenSys '22,November 6–9,2022,Boston,MA,USA Z.Shi,T.Gu,Y.Zhang and X.Zhang</header>


SenSys '22,November 6–9,2022,Boston,MA,USA


waveform in the DD domain,which reflects the changing intensity of that pulse period.


Maximum to inflection ratio (MIR):MIR is defined as the ratio of the maximum to the first inflection signal values of a pulse waveform in the DD domain,corresponding to wave reflections on arteries.


Peak-to-peak interval (PPI):PPI is a measure of the peak-to-peak interval of the pulse waveform in the DD domain,which can be used to represent a complete pulse waveform.


Expectation and variance:Expectation is the average value of a pulse waveform in the DD domain,and the variance is the amount of variability around the expectation.Both reflect the statistical features of pulse signals.


Based on the above,it is clear that these six features can comprehensively reflect the key characteristics of the pulse waveform,which is essential to realize reliable BP estimation.Note that,selecting extra features may result in an improved BP measurement,but it comes with more process complexity.


3.4.2Regression methods.The features extracted from the former step are then fed into the regression model for BP measurement.Specifically,we train the regression model to build an effective relation between the extracted features and BP values.Due to the nonlinear relationship between the extracted features and BP,the linear regression models fail to provide acceptable results.Consequently,we consider nonlinear regression models alone in this work.In the following section,we separately discuss 3widely adopted regression models:


Support Vector Machine (SVM):SVM is one of the machine learning structures,which is based on statistical learning theory [13].SVM can be used to make nonlinear decisions drawing support from the nonlinear kernels.Note that,it is also able to avoid local minima because of the attractive property:the structural risk minimization.With proper training,SVM can perform strong noise tolerance,contributing to reliable estimation results.In the training stage,the radial basis function is used as a kernel,and the size of the kernel cache is 300MB.The tolerance for stopping is set as 10−3.Decision Tree (DT):DT builds models relying on a tree structure that consists of many decision branches and nodes.The final decision is made by considering the decisions from each node and branch.DT is straightforward for understanding and interpretation,but it may fall into an over-complex structure,increasing training complexity and lowering estimation performance.In the training stage,the strategy used to choose the split at each node is set as "best",mean squared error is used as the criterion,and the maximum depth of the tree is 3.


Random Forest (RF):RF,a type of ensemble learning method,achieves the final estimation by averaging estimations from all available decision trees.Each tree is trained using the subset randomly selected from training data so as to achieve small bias and low estimation variance.Many libraries,e.g.,the Scikit-learn library,can be used for the training process.However,RF usually requires large memory for storing the data.For training stage,the number of trees in the forest is 500,and the maximum depth of each tree is 3.The mean squared error is used as the criterion.


674


Z.Shi,T.Gu,Y.Zhang and X.Zhang


Table 1:Configuration of mmWave radar


Parameters
Values
Parameters
Values
Starting Frequency
77Ghz
Bandwidth
4GHz
RX Gain
50 dB
Idle Time
10 𝜇𝑠
Chirp Cycle Time
50 𝜇𝑠
Chiprs/Frame
128
Frame Periodicity
50 ms
Samples/Chirp
256
ADC sample rate
8000K
Frequency slop
80 MHz/𝜇s



# 4PERFORMANCE EVALUATION


We now move to evaluate mmBP with a series of experiments.We first describe the experimental set-up and performance metrics,we then evaluate and benchmark mmBP with two BP standards,i.e.,the AAMI standard [53]and the BHS standard [43].We also evaluate the effectiveness of two proposed algorithms in improving the robustness of mmBP.Finally,we compare mmBP with state-ofthe-art techniques.Note that we conduct the experiments using the "subject-level split"with the leave-one-out cross-validation (LOOCV)method.


# 4.1Experimental Set-up and Metrics


We implement mmBP using a commercial-grade mmWave radar,i.e.,TI IWR1843BOOST with one transmitting (TX)antenna and four receiving (RX)antennas.The detailed configuration of the radar is given in Table 1.We use TI DCA1000board to collect raw mmWave signals,and process mmWave signals using a desktop PC with an i79750CPU and 16GB RAM.


We conduct all the experiments in a quiet room at a comfortable room temperature of 20−22Celsius degree.We recruit 25participants (11females and 14males),weighted between 48and 91kg,aged from 23to 61years old (17subjects aged $23-40$years old and 8subjects aged 41−61years old).They are university students,professions,and retirees.All of them have no health issues or chronic diseases.Data collection has been approved by the Human Research Ethics Committee of our institute.The experiment setup is shown in Fig.9,in which the subject is asked to sit on the chair with back support,make a fist,place his/her wrist and hand on the desk (purlicue facing up).A mmWave radar is set up at a very short distance (5cm)above the subject's wrist on the desk.Moreover,subjects are asked to remove any accessories (i.e.,bracelets or watches)before experiments.These operations can reduce the multipath impact and improve signal quality.For each data collection,a subject is required to keep still for 25s.There is a 10min break between two collections.We perform data collection on different days and times,and collect a total number of 100samples for each subject.To obtain the ground truth,we use an FDA-approved,arm-cuff BP measurement device (Omron HEM-7121[42]),and the subject is asked to wear the arm-cuff at the heart level for accurate data acquisition.


To evaluate BP measurement performance,we adopt three widelysed


used metrics,i.e.,Mean Error (ME),Standard Deviation of mean error


ror (STD),and Pearson's Correlation Coefficient (PCC).They are μ=


-Di一


$$\begin{array}{r}{\hat{\sum_{j=1}^{J}(\hat{b_{j}}b_{j}-b_{j})},J=\sqrt{\frac{\sum_{j=1}^{J}(\hat{b_{j}}-b_{j}-\mu)}{J}},P=\frac{\sum_{j=1}^{J}(\widehat{b_{j}}-\epsilon)(b_{j}-\kappa)}{\sqrt{\sum_{j=1}^{J}(\widehat{b_{j}}-\epsilon)^{2}}\sqrt{\sum_{j=1}^{J}(\widehat{b_{j}}-\epsilon)^{2}}\sqrt{\sum_{j=1}^{J}(b_{j}-\kappa)^{2}}},}\end{array}$$


-)( -K








where μ,σ,Pdenote ME,STD and PCC,respectively.�bjdenotes


<footer>674</footer>
<header>mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measu SenSys '22,November 6–9,2022,Boston,MA,USA</header>


mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measu




Figure 9:Experiment setup to compare mmBP with Omron device


Table 2:Performance comparison of mmBP with the AAMI standard


Method
Type
ME
(mmHg)
STD
(mmHg)
AAMI
SBP
DBP
≤5
≤8
mmBP-SVM
SBP
DBP
1.25
1.94
5.31
5.33
mmBP-DT
SBP
DBP
1.11
1.72
5.48
5.55
mmBP-RF
SBP
DBP
0.87
1.55
5.01
5.27



the estimated BP values and bjdenotes the ground truth.εis the mean of estimated BP value.Jdenotes the total number of samples,and κis the mean of the ground truth BP


# 4.2Overall Performance


To examine the performance of mmBP,Table 2compares the accuracy of mmBP using different regression models and the acceptable measurement errors standardized by the Association for the Advancement of Medical Instruments (AAMI)[53].From this table,we observe that mmBP with each regression model achieves a much smaller error for both SBP and DBP than the error boundaries regularized by the AAMI1.To further verify measurement performance,Table 3compares the accuracy of mmBP and the requirement defined in the BHS standard [43],and both SBP and DBP results reach Grade A,demonstrating that mmBP achieves high-accuracy


We then present the Bland-Altman plots of estimated SBP and DBP for mmBP with different regression models (i.e.,SVM,RF,and DT),as illustrated in Fig.10.Specifically,mmBP-SVM,mmBP-RF and mmBP-DT indicate that mmBP uses SVM,RF,and DT as regression models,respectively.The black and red lines denote ME and the limits of agreement (LOA,defined as ME±1.96×STD),respectively.We observe that among these regression models,mmBP with RF achieves the best performance.Specifically,more than 95%data of mmBP-RF is within the area of LOA,demonstrating highly


1Note that,we use AAMI as an accuracy metric to weigh the measurement results of mmBP based on the dataset collected in this


675


SenSys '22,November 6–9,2022,Boston,MA,USA


Table 3:Performance comparison of mmBP with the BHS standard


Method
Type
≤5
mmHg
≤10
mmHg
≤15
mmHg
85%
75%
65%
95%
90%
85%
BHS
Grade A
Grade B
Grade C
60%
50%
40%
mmBP-SVM
SBP
DBP
60.2%
65.9%
86.8%
93.7%
95.5%
99%
mmBP-DT
SBP
DBP
67.9%
59.6%
86.1%
81.3%
96.2%
93.6%
mmBP-RF
SBP
DBP
68.1%
61.4%
87.7%
90.1%
99.3%
99.2%



acceptable measurement results.Moreover,mmBP-RF obtains much smaller errors than the other two methods,e.g.,ME and STD of SBP at 0.87mmHg and 5.01mmHg,respectively,and ME and STD of DBP are 1.55mmHg and


To further validate mmBP,we compare PCC of SBP and DBP estimated by mmBP with the ground truth in Fig.11.As shown in this figure,mmBP (with each regression model)achieves a high correlation (at least 0.78)for both SBP and DBP.In other words,the estimated SBP and DBP are highly close to the corresponding ground truth values,verifying the effectiveness of mmBP in measurement


From the above discussion,it is obvious that mmBP is capable of accomplishing highly accurate BP measurement with various regression models.In particular,mmBP with the RF model can achieve better performance than the other two models,due to the following reasons.First,RF includes a number of regression tree learners,and each learner plays as a regression function independently.The final output of RF is obtained by averaging outputs from all individual trees.Second,RF is built with cross-validation capability with out-of-bag samples.Consequently,RF is able to reduce the bias and overall variance of the model,improving estimation performance [47].Due to the space limitation,we report the result of mmBP with the RF regression model only in the remaining


# 4.3Key Algorithm Performance


4.3.1Effectiveness of DDFT.As declared in Section 3.2,raw mmWave reflections in the time domain are usually buried into noise,leading to low SNR.To address this problem,we propose DDFT to reduce noise and improve mmWave signal quality by exploiting unique characteristics and features in the DD domain.In this section,we first evaluate DDFT in terms of SNR improvement,followed by the impact on estimation


Fig.12depicts the impact of the proposed DDFT and other three up-to-date noise reduction methods on the SNR improvement,i.e.,BW filter [1],PCA [67],and NMF [62].We find that the SNR performance of DDFT is considerably better than that of other three methods,implying that DDFT is superior in SNR improvement.This is probably because that DDFT extracts pulse-related information in the DD domain,instead of the time or frequency domains used in the existing methods.Since mmWave signals and noise show


<footer>1Note that,we use AAMI as an accuracy metric to weigh the measurement results of mmBP based on the dataset collected in this 675</footer>
<header>SenSys '22,November 6–9,2022,Boston,MA,USA Z.Shi,T.Gu,Y.Zhang and X.Zhang</header>


SenSys '22,November 6–9,2022,Boston,MA,USA


Z.Shi,T.Gu,Y.Zhang and X.Zhang




Figure 11:Pearson correlation coefficients of mmBP with various regression models


largely different features in the DD domain,it is possible to separate noise from the clean data,resulting in a better SNR


We further evaluate the impact of DDFT on estimation accuracy in Fig.13.It is clear that the curve of DDFT is significantly


676


lower than that of other three methods.In other words,DDFT contributes significantly to BP performance because it improves SNR by reducing noise in the DD


<footer>676</footer>
<header>mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measu SenSys '22,November 6–9,2022,Boston,MA,USA</header>


mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measu




Figure 12:Performance of SNR improvement with different noise reduction methods


4.3.2Effectiveness of TR-FLAF.We propose TR-FLAF to reduce the impact of tiny motions on clean signals,which exploits the nonlinear adaptive filter using the effective reference signals generated by TRSE.In this experiment,we evaluate the impact of TR-FLAF on BP


Fig.14shows the impact of TR-FLAF on measurement accuracy.Our preliminary study shows that the other two signal processing schemes do not work well,and they hence have been used as the baselines.Obviously,our TR-FLAF achieves a better result,e.g.,ME of 1.55and STD of 5.27for DBP.By contrast,ICA [31]obtains much higher errors,i.e.,5.11for ME and 8.11for STD for DBP,respectively.For NLAF [28],its ME and STD are also higher than our mmBP,i.e.,4.12and 7.07,respectively.This may be due to the high-quality reference signal generated by TR-FLAF which can effectively utilize the property of a non-linear adaptive filter to mitigate the influence of tiny motions on desired pulse-related signals.Moreover,NLAF may not be directly applied in mmWave-based BP measurement as it requires the actual pulse waveform as a reference signal which is not available due to the lack of prior knowledge of noise or pulse signals.Therefore,our TR-FLAF is significant in achieving reliable BP measurement


# 4.4Robustness Analysis


It is well known that the robustness of BP measurement is an essential factor for real deployment.In this section,we evaluate and analyze the robustness of mmBP under various parameter settings and


4.4.1Impact of measurement distance.The distance between mmWave radar and the subject may affect the performance of mmBP,mainly due to the multipath impact and noise.In this experiment,we evaluate measurement accuracy with various distances,as shown in Fig.15.We consider six distances,and at each distance,we estimate BP values using the model trained with 5cm dataset.As can be observed,estimation error goes up with the distance.This is because a longer distance may lead to more severe multipath impact and noise.Consequently,it is harder to extract useful features with an increased distance.Note that our recommended distance is 5cm to reduce these negative impacts.This figure also verifies that the estimation result with such a distance is highly accurate.Moreover,


677


SenSys '22,November 6–9,2022,Boston,MA,USA




Figure 13:Impact of noise reduction methods on BP measurement accuracy




Figure 14:Impact of motion compensation methods on BP measurement accuracy


it is clear that the estimation error of mmBP still meets the specification of AAMI boundary when the distance is up to 20cm.In other words,mmBP achieves fairly reliable BP measurement with the measurement distance up to 20cm,which is of significance to practical


4.4.2Impact of measurement time.In this experiment,we evaluate the impact of measurement time which indicates the duration of each BP measurement.Fig.16shows the measurement accuracy with measurement time.As we observe,longer measurement time results in better performance,i.e.,smaller MEs for both SBP and DBP.This is due to the fact that the more data we collect,the more pulse waveform-based features we can exploit.Another interesting observation is that the tendency of error performance becomes flat after a threshold.Moreover,prolong measurement may make subjects uncomfortable as they are required to remain stationary during data collection.Hence,we set the measurement time as 25s to trade off measurement accuracy and user


# 4.5Comparison against the state-of-the-arts


In this section,we compare mmBP with four baseline systems–Blumio [34],SBPM [49],MMW [24]and CBPE [25],in terms of estimation errors,comfort level,calibration,and motion robustness based on the results reported in each of these


First,as shown in Table 4,mmBP is superior to other four methods in terms of measurement accuracy.Specifically,mmBP achieves a mean error of 0.87mmHg and 1.55mmHg for SBP and DBP,respectively,which are dramatically smaller than other methods


<footer>677</footer>
<header>Z.Shi,T.Gu,Y.Zhang and X.Zhang SenSys '22,November 6–9,2022,Boston,MA,USA</header>


SenSys '22,November 6–9,2022,Boston,MA,USA




Figure 15:Performance of mmBP with different measurement distances




Figure 16:Performance of mmBP with different measurement time


≥1.7for SBP and ≥2.85for DBP in Blumio).Moreover,mmBP outperforms other methods in terms of STD,i.e.,mmBP achieves a STD of 5.01mmHg and 5.27mmHg for SBP and DBP,respectively,while the best result reported in other works (i.e.,in Blumio)is 5.59mmHg and 5.57mmHg for SBP and DBP,respectively.It is noteworthy that Blumio relies on calibration for BP measurement,which can be seen as a "user-dependent"method and may incur more processing complexity.Second,mmBP is highly robust against small-scale and tiny human motions,which is essential for practical deployment,while motion robustness in all other methods remains


Apart from the drawbacks in accuracy and robustness,the four existing systems may suffer from other limitations.To be specific,Blumio requires subject to wear a mmWave radar device on wrist and secure it with a medical adhesive patch,which may not be user-friendly for practical use.Moreover,the requirement of calibration is another issue restricting its application potential.SBPM focuses on SBP estimation only but no study reported for DBP.Note that,DBP is also an essential factor for BP measurement,and measuring DBP is more challenging than SBP.MMW and CBPE report feasibility studies of BP measurement using mmWave radar.Both studies demonstrate that cardiac movement can be used for


678


Z.Shi,T.Gu,Y.Zhang and X.Zhang


BP measurement due to the correlation between cardiac activities and BP values,however,their studies are preliminary as they neither design any specific measurement methods nor report specific measurement accuracy.mmBP presents a novel system design to achieve high accuracy in a fully contactless and calibration-free manner,and it is also highly robust to tiny


# 5DISCUSSION AND FUTURE WORK


Evaluation on clinic setting:mmBP can achieve accurate and robust BP measurement with the dataset collected from 25normal subjects.It demonstrates the effectiveness in everyday-use health monitoring application for healthy users with normal BP ranges.To improve usability,we will extend the evaluation of mmBP to clinic settings,e.g.,enriching diversity in measurement cases,enlarging the size of dataset and expanding age


Large-scale motions:mmBP uses a novel motion compensation scheme (TF-FLAF)to reduce the impact of tiny motions (i.e.,small scale motions)on pulse waveform construction.In the current study,subjects are required to keep stationary to avoid large-scale movements during measurement.However,accommodating largescale motions can further improve the robustness.We will further enhance the robustness of mmBP by handling large-scale motions during measurement in our future work,and this can be potentially achieved by exploiting the variations of mmWave signals (e.g.,phase information)contained in different range bins


Measurement posture and position:mmBP requires subject to make a fist and place his/her hand and wrist on table (purlicue facing up).Note that,the posture or the angle between wrist and table may be slightly different for multiple measurements or subjects,which is tolerable and has been included in the dataset.Moreover,mmBP chooses the subject's wrist for measurement,and measurement position may affect performance due to the quality of mmWave reflections received from different body positions.To improve usability,we plan to evaluate different measurement positions such as upper arm or neck by trading off accuracy and user experience in our future


# 6RELATED WORK


In this section,we review existing BP measurement methods,highlight their properties and compare the pros and


Direct BP measurement is achieved by catheterization [18].The procedure is invasive as it is usually conducted in arterial line,providing real-time and instantaneous BP values with heartbeat [16].Since this method can estimate BP directly and accurately,it is regarded as the "gold standard"BP measurement.However,this method can only be performed through medical intervention,and a particular medical device (e.g.,cannula needle)will be placed in subject's artery,causing discomfort and a risk of infection [30].The direct BP measurement is usually restricted to surgical interventions in hospitals,thus it is not suitable for daily measurement at home.Cuff-based BP measurement has received popularity as a viable,non-invasive BP measurement method.The idea is to detect SBP and DBP through the inflation and deflation of an inflatable cuf carried on the arm or finger of subject.This method is commonly


<footer>678</footer>
<header>mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measu SenSys '22,November 6–9,2022,Boston,MA,USA</header>


mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measu


SenSys '22,November 6–9,2022,Boston,MA,USA


Table 4:Performance comparison of mmWave-based BP measurements


Method
Blumio [34]
SBPM [49]
MMW [24]
CBPE [25]
mmBP
SBP ME± STD(mmHg)
1.70±5.59
2±N/A
N/A
N/A
0.87± 5.01
DBP ME± STD(mmHg)
2.85± 5.57
N/A
N/A
N/A
1.55± 5.27
Device
Blumio sensor
IWR-6843AOP
MMW sensor
MMW sensor
IWR-1843
Comfort level
Middle
High
High
High
High
Calibration
Yes
No
No
No
No
Motion robustness
Low
Low
Middle
Middle
High



used in clinical and home settings such as classical mercury or electronic sphygmomanometers $[8,12]$.However,during measurement,subject may feel uncomfortable or even painful when inflating cuff.Wearable BP measurement typically uses wearable devices (e.g.,wristwatch)[7,22,23,58]which can be done continuously as long as subject carries the device.Thomas et al.[58]propose a BP sensing system using ECG and PPG to measure the proximal timing and distal timing of the blood flows,respectively.Andrew et al.[7]use an accelerometer to measure the proximal timing,and the distal timing is obtained by PPG.Wrist-worn device has been proposed in $\left[21\right]$,and bioimpedance (BI)is used to determine pulse transit time (PTT)for BP measurement.While promising,some challenges remain unsolved.To name a few,the sensing performance of these methods is very sensitive to device placement,i.e.,a tiny mismatch in placement may lead to dramatic performance degradation.In addition,PPG-based methods are vulnerable to the interference induced by ambient conditions or skin tattoos [5].


Video/Image based BP measurement has become prevalent in recent years.Video/image captured by camera is processed to extract effective features for BP measurement.In other words,the reaction of lights (e.g.,the absorption and reflection)on the interested region of human body is exploited to estimate BP values [48,54,55].Sugita et al.[54]investigate video plethysmogram (VPG)collected from the hand palm of subject.With VPG,an effective relationship between the internal pressure and blood vessels can be built,achieving successful BP measurement.Secerbegovic et al.[48]use a digital camera to extract VPG from the forehead of subject.The captured VPG is then used to calculate PTT and ECG,achieving BP measurement.Similarly,Sugita et al.[55]obtain VPG from the cheek of subject,and apply PTT and VPG for BP measurement.Despite their merits,camera-based methods have stringent requirements on light conditions and may raise privacy concerns.


Radio frequency based BP measurement leverages the variations of radio frequency signals exerted by blood flows [27,68].Kim et al.[27]design an radio frequency based system to estimate BP in a contact-free manner.A sensor system is placed in front of a subject to collect and process UWB signals to extract key features related to BP measurement.Zhao et al.[68]develop a Doppler radar based BP measurement system.The system is placed 0.5m away from subject for continuous wave (CW)collection and processing.These systems enable contact-free BP measurement,however,their performance may not be satisfactory in reality due to low frequency and narrow bandwidth.


mmWave based BP measurement has been recently promising due to its higher frequency and wider bandwidth.mmWave sensing is able to detect small variations of physiological signals


679


(less than 1mm)which are closely related to BP measurement (e.g.,pulse waveform),hence BP measurement can be achieved using extracted pulse information.Only a few works have investigated this direction.Yamaoka et al.[64]conduct experimental study to demonstrate that variations of mmWave signal power are related to BP changes,but the specific relationship is yet to investigate.Kawasaki et al.[24,25]perform feasibility studies of mmWavebased BP measurement,in which mmWave sensors are used to extract time-domain features to estimate BP values.These solutions are initial attempts to utilize the property of mmWave signals for BP measurement,while they did not design any specific measurement methods or report any specific measurement accuracy.With the similar purpose,Shi et al.[49]investigate SBP estimation by leveraging the property of mmWave reflection.However,they did not take DBP estimation into consideration,which is a critical factor for reliable BP measurement and is usually more challenging to achieve.Liao et al.[34]design a wearable mmWave system that requires a mmWave sensor wrapped on subject's wrist to receive reflected mmWave signals.However,wrapping sensor on subject's wrist may cause discomfort.Another concern is that the subject is required to provide the actual BP values for calibration,which is not realistic in practical applications.Additionally,all the existing mmWave based BP measurement methods are always sensitive to ambient noise and tiny motions.Signal processing methods such as filter or signal decomposition can partially address this problem,however,residual noise and tiny motion still remain in mmWave reflections,resulting in difficulty in pulse waveform construction.


# 7CONCLUSION


This paper presents a novel contact-free mmWave-based BP measurement system by exploiting effective features in the DD domain to foster accurate,motion-robust and comfortable BP measurement.We propose a novel method to reduce noise influence on pulse waveform construction,by leveraging the property of mmWave signals in the DD domain.To address non-linear interference caused by human's tiny motions,we develop a novel motion compensation scheme in which an effective reference signal can be produced based on the periodic and correlation characteristics of pulse signals.Extensive evaluations are conducted with a range of scenarios,and results show that mmBP is able to achieve highly accurate and motion-robust BP measurement.mmBP can be potentially deployed in a wide range of day-to-day BP measurement scenarios.


# REFERENCES


[1]Fahd A.Alturki,Majid Aljalal,Akram M.Abdurraqeeb,Khalil Alsharabi,and Abdullrahman A.Al-Shamma'a.2021.Common Spatial Pattern Technique With


<footer>679</footer>
<header>SenSys '22,November 6–9,2022,Boston,MA,USA Z.Shi,T.Gu,Y.Zhang and X.Zhang</header>


SenSys '22,November 6–9,2022,Boston,MA,USA


EEG Signals for Diagnosis of Autism and Epilepsy Disorders.IEEE Access 9(2021),24334–24349.https://doi.org/10.1109/ACCESS.2021.3056619
[2]Ahmad Anouti and William C Koller.1995.Tremor disorders.Diagnosis and management.Western journal of medicine 162,6(1995),510.
[3]Daniel Barvik,Martin Cerny,Marek Penhaker,and Norbert Noury.2022.Noninvasive Continuous Blood Pressure Estimation From Pulse Transit Time:A Review of the Calibration Models.IEEE Reviews in Biomedical Engineering 15(2022),138–151.https://doi.org/10.1109/RBME.2021.3109643
[4]Fabian Beutel,Chris Van Hoof,Xavier Rottenberg,Koen Reesink,and Evelien Hermeling.2021.Pulse Arrival Time Segmentation Into Cardiac and Vascular Intervals –Implications for Pulse Wave Velocity and Blood Pressure Estimation.IEEE Transactions on Biomedical Engineering 68,9(2021),2810–2820.https://doi.org/10.1109/TBME.2021.3055154
[5]Mark Butlin,Fatemeh Shirbani,Edward Barin,Isabella Tan,Bart Spronck,and Alberto P.Avolio.2018.Cuffless Estimation of Blood Pressure:Importance of Variability in Blood Pressure Dependence of Arterial Stiffness Across Individuals and Measurement Sites.IEEE Transactions on Biomedical Engineering 65,11(2018),2377–2383.https://doi.org/10.1109/TBME.2018.2823333
[6]Dilpreet Buxi,Jean-Michel Redouté,and Mehmet Rasit Yuce.2017.Blood Pressure Estimation Using Pulse Transit Time From Bioimpedance and Continuous Wave Radar.IEEE Transactions on Biomedical Engineering 64,4(2017),917–927.https://doi.org/10.1109/TBME.2016.2582472
[7]Andrew M.Carek,Jordan Conant,Anirudh Joshi,Hyolim Kang,and Omer T.Inan.2017.SeismoWatch:Wearable Cuffless Blood Pressure Monitoring Using Pulse Transit Time.Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.1,3,Article 40(sep 2017),16pages.https://doi.org/10.1145/3130905
[8]Ayan Chakraborty,Dharitri Goswami,Jayanta Mukhopadhyay,and Saswat Chakrabarti.2021.Measurement of Arterial Blood Pressure Through Single-Site Acquisition of Photoplethysmograph Signal.IEEE Transactions on Instrumentation and Measurement 70(2021),1–10.https://doi.org/10.1109/TIM.2020.3011304
[9]Vikram Chandrasekaran,Ram Dantu,Srikanth Jonnada,Shanti Thiyagaraja,and Kalyan Pathapati Subbu.2013.Cuffless Differential Blood Pressure Estimation Using Smart Phones.IEEE Transactions on Biomedical Engineering 60,4(2013),1080–1089.https://doi.org/10.1109/TBME.2012.2211078
[10]Anand Chandrasekhar,Mohammad Yavarimanesh,Keerthana Natarajan,JinOh Hahn,and Ramakrishna Mukkamala.2020.PPG Sensor Contact Pressure Should Be Taken Into Account for Cuff-Less Blood Pressure Measurement.IEEE Transactions on Biomedical Engineering 67,11(2020),3134–3140.https://doi.org/10.1109/TBME.2020.2976989
[11]Zhe Chen,Tianyue Zheng,Chao Cai,and Jun Luo.2021.MoVi-Fi:Motion-Robust Vital Signs Waveform Recovery via Deep Interpreted RF Sensing.In Proceedings of the 27th Annual International Conference on Mobile Computing and Networking (New Orleans,Louisiana)(MobiCom '21).Association for Computing Machinery,New York,NY,USA,392–405.https://doi.org/10.1145/3447993.3483251
[12]Juan Cheng,Yufei Xu,Rencheng Song,Yu Liu,Chang Li,and Xun Chen.2021.Prediction of arterial blood pressure waveforms from photoplethysmogram signals via fully convolutional neural networks.Computers in Biology and Medicine 138(2021),104877.https://doi.org/10.1016/j.compbiomed.2021.104877
[13]Corinna Cortes and Vladimir Vapnik.1995.Support-vector networks.Machine learning 20,3(1995),273–297.
[14]George Cybenko.1989.Approximation by superpositions of a sigmoidal function.Mathematics of control,signals and systems 2,4(1989),303–314.
[15]Günther Deuschl,Peter Bain,Mitchell Brin,and Ad Hoc Scientific Committee.1998.Consensus Statement of the Movement Disorder Society on Tremor.Movement Disorders 13,S3(1998),2–23.https://doi.org/10.1002/mds.870131303
[16]C El-Hajj and PA Kyriacou.2021.Deep learning models for cuffless blood pressure monitoring from PPG signals using attention mechanism.Biomedical Signal Processing and Control 65(2021),102301.https://doi.org/10.1016/j.bspc.2020.102301
[17]Yariv Ephraim and Harry L Van Trees.1995.A signal subspace approach for speech enhancement.IEEE Transactions on speech and audio processing 3,4(1995),251–266.
[18]L.A.Geddes.2013.Handbook of Blood Pressure Monitoring.Springer Sceience and Business Media (2013).
[19]Unsoo Ha,Salah Assana,and Fadel Adib.2020.Contactless Seismocardiography via Deep Learning Radars.Association for Computing Machinery,New York,NY,USA.https://doi.org/10.1145/3372224.3419982
[20]R.Hadani,S.Rakib,M.Tsatsanis,A.Monk,A.J.Goldsmith,A.F.Molisch,and R.Calderbank.2017.Orthogonal Time Frequency Space Modulation.In 2017IEEE Wireless Communications and Networking Conference (WCNC).1–6.https://doi.org/10.1109/WCNC.2017.7925924
[21]Toan Huynh,Roozbeh Jafari,and Wan-Young Chung.2018.A Robust Bioimpedance Structure for Smartwatch-Based Blood Pressure Monitoring.Sensors 18(062018),2095.https://doi.org/10.3390/s18072095
[22]Toan Huynh,Roozbeh Jafari,and Wan-Young Chung.2018.Noninvasive Cuffless Blood Pressure Estimation Using Pulse Transit Time and Impedance Plethysmography.IEEE Transactions on Biomedical Engineering PP (082018),


680


Z.Shi,T.Gu,Y.Zhang and X.Zhang


[23]Jessi E.Johnson,Oliver Shay,Chris Kim,and Catherine Liao.2019.Wearable Millimeter-Wave Device for Contactless Measurement of Arterial Pulses.IEEE Transactions on Biomedical Circuits and Systems 13,6(2019),1525–1534.https://doi.org/10.1109/TBCAS.2019.2948581
[24]Ryota Kawasaki and Akihiro Kajiwara.2021.Continuous blood pressure monitoring with MMW radar sensor.IEICE Communications Express 10,12(2021),997–1002.https://doi.org/10.1587/comex.2021XBL0156
[25]Ryota Kawasaki and Akihiro Kajiwara.2022.Continuous blood pressure estimation using millimeter wave radar.In 2022IEEE Radio and Wireless Symposium (RWS).135–137.https://doi.org/10.1109/RWS53089.2022.9719965
[26]Chang-Sei Kim,Andrew M.Carek,Omer T.Inan,Ramakrishna Mukkamala,and Jin-Oh Hahn.2018.Ballistocardiogram-Based Approach to Cuffless Blood Pressure Monitoring:Proof of Concept and Potential Challenges.IEEE Transactions on Biomedical Engineering 65,11(2018),2384–2391.https://doi.org/10.1109/TBME.2018.2797239
[27]Insoo Kim and Yusuf A.Bhagat.2016.Towards development of a mobile RF Doppler sensor for continuous heart rate variability and blood pressure monitoring.In 201638th Annual International Conference of the IEEE Engineering in Medicine and Biology Society (EMBC).3390–3393.https://doi.org/10.1109/EMBC.2016.7591455
[28]Shunsuke Koshita,Masahide Abe,and Masayuki Kawamata.2018.Recent advances in variable digital filters.Digital Systems (2018).
[29]Timo Lauteslager,Mathias Tommer,Tor Sverre Lande,and Timothy G.Constandinou.2019.Coherent UWB Radar-on-Chip for In-Body Measurement of Cardiovascular Dynamics.IEEE Transactions on Biomedical Circuits and Systems 13,5(2019),814–824.https://doi.org/10.1109/TBCAS.2019.2922775
[30]Tai Le,Floranne Ellington,Tao-Yi Lee,Khuong Vo,Michelle Khine,Sandeep Kumar Krishnan,Nikil Dutt,and Hung Cao.2020.Continuous Non-Invasive Blood Pressure Monitoring:A Methodological Review on Measurement Techniques.IEEE Access 8(2020),212478–212498.https://doi.org/10.1109/ACCESS.2020.3040257
[31]Jongshill Lee,Minseong Kim,Hoon-Ki Park,and In Young Kim.2020.Motion Artifact Reduction in Wearable Photoplethysmography Based on Multi-Channel Sensors with Multiple Wavelengths.Sensors 20,5(2020).https://doi.org/10.3390/s20051493
[32]Kwonjoon Lee and Hoi-Jun Yoo.2021.Simultaneous Electrical Bio-Impedance Plethysmography at Different Body Parts:Continuous and Non-Invasive Monitoring of Pulse Wave Velocity.IEEE Transactions on Biomedical Circuits and Systems 15,5(2021),1027–1038.https://doi.org/10.1109/TBCAS.2021.3115021
[33]Chengcai Leng,Hai Zhang,Guorong Cai,Zhen Chen,and Anup Basu.2021.Total Variation Constrained Non-Negative Matrix Factorization for Medical Image Registration.IEEE/CAA Journal of Automatica Sinica 8,5(2021),1025–1037.https://doi.org/10.1109/JAS.2021.1003979
[34]Catherine Liao,Oliver Shay,Elizabeth Gomes,and Nikhil Bikhchandani.2021.Noninvasive Continuous Blood Pressure Measurement with Wearable Millimeter Wave Device.In 2021IEEE 17th International Conference on Wearable and Implantable Body Sensor Networks (BSN).1–5.https://doi.org/10.1109/BSN51625.2021.9507020
[35]Jing Liu,Bryan Yan,Shih-Chi Chen,Yuan-Ting Zhang,Charles Sodini,and Ni Zhao.2021.Non-Invasive Capillary Blood Pressure Measurement Enabling Early Detection and Classification of Venous Congestion.IEEE Journal of Biomedical and Health Informatics 25,8(2021),2877–2886.https://doi.org/10.1109/JBHI.2021.3055760
[36]Shing-Hong Liu,Jia-Jung Wang,and Kuo-Sheng Huang.2008.A New Oscillometry-Based Method for Estimating the Brachial Arterial Compliance Under Loaded Conditions.IEEE Transactions on Biomedical Engineering 55,10
(2008),2463–2470.https://doi.org/10.1109/TBME.2008.925711
[37]Elan D.Louis.2001.Essential Tremor.New England Journal of Medicine 345,12(2001),887–891.https://doi.org/10.1056/NEJMcp010928arXiv:https://doi.org/10.1056/NEJMcp010928PMID:11565522.
[38]Sarmad Malik,Jason Wung,Josh Atkins,and Devang Naik.2020.Double-Talk Robust Multichannel Acoustic Echo Cancellation Using Least-Squares MIMO Adaptive Filtering:Transversal,Array,and Lattice Forms.IEEE Transactions on Signal Processing 68(2020),4887–4902.https://doi.org/10.1109/TSP.2020.3011572
[39]Hafiz Shakir Mehmood,Rana Zeeshan Ahmad,and M Jehanzaib Yousuf.2019.A comprehensive review of adaptive noise cancellation techniques in the internet of things.In Proceedings of the 3rd international conference on future networks and distributed systems.1–8.
[40]Cristina I.Muresan,Isabela R.Birs,Eva H.Dulf,Dana Copot,and Liviu Miclea.2021.A Review of Recent Advances in Fractional-Order Sensing and Filtering Techniques.Sensors 21,17(2021).https://doi.org/10.3390/s21175920
[41]Keerthana Natarajan,Robert C.Block,Mohammad Yavarimanesh,Anand Chandrasekhar,Lalit K.Mestha,Omer T.Inan,Jin-Oh Hahn,and Ramakrishna Mukkamala.2022.Photoplethysmography Fast Upstroke Time Intervals Can Be Useful Features for Cuff-Less Measurement of Blood Pressure Changes in Humans.IEEE Transactions on Biomedical Engineering 69,1(2022),


<footer>680</footer>
<header>mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measu SenSys '22,November 6–9,2022,Boston,MA,USA</header>


mmBP:Contact-free Millimetre-wave Radar based Approach to Blood Pressure Measu


[42]Omron.2015.https://www.omronhealthcare-ap.com/au/product/128-hem-7121.(2015).[43]Eoin O'Brien,James Petrie,WA Littler,Michael De Swiet,Paul L Padfield,Douglas Altman,Martin Bland,Andrew Coats,Neil Atkins,et al.1993.The British Hypertension Society protocol for the evaluation of blood pressure measuring devices.J hypertens 11,Suppl 2(1993),S43–S62.
[44]Jagdish C Patra and Alex C Kot.2002.Nonlinear dynamic system identification using Chebyshev functional link artificial neural networks.IEEE Transactions on Systems,Man,and Cybernetics,Part B (Cybernetics)32,4(2002),505–511.
[45]David Perpetuini,Daniela Cardone,Chiara Filippini,Antonio Maria Chiarelli,and Arcangelo Merla.2021.A Motion Artifact Correction Procedure for fNIRS Signals Based on Wavelet Transform and Infrared Thermography Video Tracking.Sensors 21,15(2021).https://doi.org/10.3390/s21155117
[46]Rakesh Ranjan,Bikash Chandra Sahana,and Ashish Kumar Bhandari.2022.Motion Artifacts Suppression From EEG Signals Using an Adaptive Signal Denoising Method.IEEE Transactions on Instrumentation and Measurement 71(2022),1–10.https://doi.org/10.1109/TIM.2022.3142037
[47]V Rodriguez-Galiano,M Sanchez-Castillo,M Chica-Olmo,and MJOGR ChicaRivas.2015.Machine learning predictive models for mineral prospectivity:An evaluation of neural networks,random forest,regression trees and support vector machines.Ore Geology Reviews 71(2015),804–818.
[48]A.Secerbegovic,J.Bergsland,P.S.Halvorsen,N.Suljanovic,A.Mujcic,and I.Balasingham.2016.Blood pressure estimation using video plethysmography.In 2016IEEE 13th International Symposium on Biomedical Imaging (ISBI).461–464.https://doi.org/10.1109/ISBI.2016.7493307
[49]JingYao Shi and KangYoon Lee.2022.Systolic blood pressure measurement algorithm with mmWave radar sensor.KSII Transactions on Internet and Information Systems (TIIS)16,4(2022),1209–1223.
[50]Sungtae Shin,Azin Sadat Mousavi,Sophia Lyle,Elisabeth Jang,Peyman Yousefian,Ramakrishna Mukkamala,Dae-Geun Jang,Ui Kun Kwon,Youn Ho Kim,and Jin-Oh Hahn.2022.Posture-Dependent Variability in Wrist BallistocardiogramPhotoplethysmogram Pulse Transit Time:Implication to Cuff-Less Blood Pressure Tracking.IEEE Transactions on Biomedical Engineering 69,1(2022),347–355.https://doi.org/10.1109/TBME.2021.3094200
[51]C Shraddha,ML Chayadevi,and MA Anusuya.2019.Noise cancellation and noise reduction techniques:A review.In 20191st International Conference on Advances in Information Technology (ICAIT).IEEE,159–166.
[52]Kwai Sang Sin.1981.Adaptive filtering,prediction and control.University of Newcastle.
[53]George S Stergiou,Bruce Alpert,Stephan Mieke,Roland Asmar,Neil Atkins,Siegfried Eckert,Gerhard Frick,Bruce Friedman,Thomas Graßl,Tsutomu Ichikawa,et al.2018.A universal standard for the validation of blood pressure measuring devices:Association for the Advancement of Medical Instrumentation/European Society of Hypertension/International Organization for Standardization (AAMI/ESH/ISO)Collaboration Statement.Hypertension 71,3
(2018),368–374.
[54]Norihiro Sugita,Taihei Noro,Makoto Yoshizawa,Kei Ichiji,Shunsuke Yamaki,and Noriyasu Homma.2019.Estimation of Absolute Blood Pressure Using Video Images Captured at Different Heights from the Heart.In 201941st Annual International Conference of the IEEE Engineering in Medicine and Biology Society (EMBC).4458–4461.https://doi.org/10.1109/EMBC.2019.8856362
[55]Norihiro Sugita,Makoto Yoshizawa,Makoto Abe,Akira Tanaka,Noriyasu Homma,and Tomoyuki Yambe.2019.Contactless Technique for Measuring BloodPressure Variability from One Region in Video Plethysmography.Chinese Journal of Medical and Biological Engineering (Feb 2019).https://doi.org/10.1007/s40846-018-0388-8
[56]Shinobu Tanaka,Masamichi Nogawa,Takehiro Yamakoshi,and Ken-ichi Yamakoshi.2007.Accuracy Assessment of a Noninvasive Device for Monitoring Beat-by-Beat Blood Pressure in the Radial Artery Using the VolumeCompensation Method.IEEE Transactions on Biomedical Engineering 54,10
(2007),1892–1895.https://doi.org/10.1109/TBME.2007.894833
[57]Bhomraj Thanvi,Nelson Lo,and Tom Robinson.2006.Essential tremor—the most common movement disorder in older people.Age and Ageing 35,4(042006),344–349.https://doi.org/10.1093/ageing/afj072arXiv:https://academic.oup.com/ageing/article-pdf/35/4/344/50737/afj072.pdf
[58]Simi Thomas,Viswam Nathan,Chengzhi Zong,Ebunoluwa Akinbola,Antoine Lourdes Praveen Aroul,Lijoy Philipose,Karthikeyan Soundarapandian,Xiangrong Shi,and Roozbeh Jafari.2014.BioWatch -A wrist watch based signal acquisition system for physiological signals including blood pressure.201436th Annual International Conference of the IEEE Engineering in Medicine and Biology Society,EMBC 20142014,2286–9.https://doi.org/10.1109/EMBC.2014.6944076
[59]Leila Tlebaldiyeva,Behrouz Maham,and Theodoros A.Tsiftsis.2019.Device-toDevice mmWave Communication in the Presence of Interference and Hardware Distortion Noises.IEEE Communications Letters 23,9(2019),1607–1610.https://doi.org/10.1109/LCOMM.2019.2922905
[60]Edward Jay Wang,Junyi Zhu,Mohit Jain,Tien-Jui Lee,Elliot Saba,Lama Nachman,and Shwetak N.Patel.2018.Seismo:Blood Pressure Monitoring Using Builtin Smartphone Accelerometer and Camera (CHI '18).Association for Computing


681


SenSys '22,November 6–9,2022,Boston,MA,USA


Machinery,New York,NY,USA,1–9.https://doi.org/10.1145/3173574.3173999
[61]Fengyu Wang,Xiaolu Zeng,Chenshu Wu,Beibei Wang,and KJ Ray Liu.2021.Driver vital signs monitoring using millimeter wave radio.IEEE Internet of Things Journal (2021).
[62]Taihui Wang,Feiran Yang,and Jun Yang.2022.Convolutive Transfer FunctionBased Multichannel Nonnegative Matrix Factorization for Overdetermined Blind Source Separation.IEEE/ACM Transactions on Audio,Speech,and Language Processing 30(2022),802–815.https://doi.org/10.1109/TASLP.2022.3145304
[63]Ke Xu,Xinyu Jiang,and Wei Chen.2020.Photoplethysmography Motion Artifacts Removal Based on Signal-Noise Interaction Modeling Utilizing Envelope Filtering and Time-Delay Neural Network.IEEE Sensors Journal 20,7(2020),3732–3744.https://doi.org/10.1109/JSEN.2019.2960370
[64]Yukino Yamaoka,Jiang Liu,and Shirgeru Shimamoto.2019.Detections of pulse and blood pressure employing 5G millimeter wave signal.In 201916th IEEE Annual Consumer Communications Networking Conference (CCNC).1–2.https://doi.org/10.1109/CCNC.2019.8651697
[65]Mohammad Yavarimanesh,Robert C.Block,Keerthana Natarajan,Lalit K.Mestha,Omer T.Inan,Jin-Oh Hahn,and Ramakrishna Mukkamala.2022.Assessment of Calibration Models for Cuff-Less Blood Pressure Measurement After One Year of Aging.IEEE Transactions on Biomedical Engineering 69,6(2022),2087–2093.https://doi.org/10.1109/TBME.2021.3136492
[66]Xin Zhang,Xinwei Jiang,Junjun Jiang,Yongshan Zhang,Xiaobo Liu,and Zhihua Cai.2022.Spectral–Spatial and Superpixelwise PCA for Unsupervised Feature Extraction of Hyperspectral Imagery.IEEE Transactions on Geoscience and Remote Sensing 60(2022),1–10.https://doi.org/10.1109/TGRS.2021.3057701
[67]Zezhong Zhang,Guangxu Zhu,Rui Wang,Vincent K.N.Lau,and Kaibin Huang.2022.Turning Channel Noise into an Accelerator for Over-the-Air Principal Component Analysis.IEEE Transactions on Wireless Communications (2022),1–1.https://doi.org/10.1109/TWC.2022.3162868
[68]Heng Zhao,Xu Gu,Hong Hong,Yusheng Li,Xiaohua Zhu,and Changzhi Li.2018.Non-contact Beat-to-beat Blood Pressure Measurement Using Continuous Wave Doppler Radar.In 2018IEEE/MTT-S International Microwave Symposium -IMS.1413–1415.https://doi.org/10.1109/MWSYM.2018.8439354
[69]Tianyue Zheng,Zhe Chen,Shujie Zhang,Chao Cai,and Jun Luo.2021.MoRe-Fi:Motion-Robust and Fine-Grained Respiration Monitoring via Deep-Learning UWB Radar.In Proceedings of the 19th ACM Conference on Embedded Networked Sensor Systems (Coimbra,Portugal)(SenSys '21).Association for Computing Machinery,New York,NY,USA,


<footer>681</footer>
