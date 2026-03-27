<header>IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20 518</header>


518


IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20


# mmBP+:Contact-Free Blood Pressure Measurement Using Millimeter-Wave Radar


Zhenguo Shi ,Member,IEEE,Tao Gu ,Fellow,IEEE,Yu Zhang ,Member,IEEE,and Xi Zhang


Abstract—Blood pressure (BP)measurement is an indispensable tool in diagnosing and treating many diseases such as cardiovascular failure and stroke.Traditional direct measurement can be invasive,and wearable-based methods may have limitations of discomfort and inconvenience.Contact-free BP measurement has been recently advocated as a promising alternative.In particular,Millimeter-wave (mmWave)sensing has demonstrated its promising potential,however it is confronted with several challenges including noise and vulnerability to human's tiny motions which may occur intentionally and inevitably.In this paper,we propose mmBP+,a contact-free mmWave-based BP measurement system with high accuracy and motion robustness.Due to the high frequency and short wavelength,mmWave signals received in the time domain are dramatically susceptible to ambient noise,and deteriorating signal quality.To reduce noise,we propose a novel approach to exploit mmWave signal's characteristics and features in the delay-Doppler-fractional Fourier domain to significantly improve signal quality for pulse waveform construction.We also propose a periodic signal feature based functional link adaptive filter leveraging on the periodic and correlation characteristics of pulse waveform signals to alleviate the impact of human's tiny motions.Extensive experiment results achieved by the leave-oneout cross-validation (LOOCV)method demonstrate that mmBP+achieves the mean errors of 0.65mmHg and 1.31mmHg for systolic blood pressure (SBP)and diastolic blood pressure (DBP),respectively;and the standard deviation errors of 3.92mmHg and 3.99mmHg for SBP and DBP,


Index Terms—Blood pressure (BP),contact-free sensing,MmWave radar,wireless


# I.INTRODUCTION


B LOOD pressure (BP),a periodic signal exerted by heartbeats,is one of the most representative physiological signs of human beings.BP is also a crucial indicator for physicians to diagnosecardiovascular conditions andtreat relateddiseases [1].A human's blood pressure goes up and down between the maximum blood pressure,i.e.,systolic blood pressure (SBP),


Received 22January 2025;revised 18June 2025;accepted 24July 2025.
Date of publication 31July 2025;date of current version 3December 2025.Recommended for acceptance by W.Gong.(Corresponding author:Tao Gu.)This work involved human subjects or animals in its research.Approval of all ethical and experimental procedures and protocols was granted by the Science &Engineering Subcommittee,Macquarie University under Application No.520221141241381,and performed in line with the National Statement on Ethical Conduct in Human Research 2007.
Zhenguo Shi is with the School of Computer Science and Engineering,University of New South Wales,Sydney 2052,Australia (e-mail:shizhenguotvt @gmail.com).
Tao Gu,Yu Zhang,and Xi Zhang are with the School of Computing,Macquarie University,Sydney 2109,Australia (e-mail:tao.gu@mq.edu.au;y.zhang@mq.edu.au;zaibuer@gmail.com).
Digital Object Identifier


and the minimum pressure,i.e.,diastolic blood pressure (DBP),reflecting valuable information about health condition.BP measurement has become significantly important to our daily life,hence receiving particular interest from both academia and


Among a range of BP measurement methods developed over decades,the "gold standard"is direct BP measurement using particular medical devices placed into the arterial line of subject [2].Although it achieves high accuracy,this method is invasive,causing pain or risk of infection.Non-invasive BP measurement has been advocated as a safe and convenient alternative,hence attracting increasing attention.In such a context,BPmeasurementcanbeaccomplishedbyexploitingtheproperty of physiological characteristics.In particular,pulse wave has been widely used for BP measurement as it essentially contains adequate BP-related features,e.g.,peak value,minimum value,andfirstinflection[3].Withpulsewaveformanalysistechniques,these features can be processed to build an effective relationship between pulse waveform and BP values,achieving successful BP measurements.Towards this end,several BP measurement methods have been proposed to capture pulse-related physiological signals,e.g.,Photoplethysmography (PPG)[4],using dedicateddevicessuchaswrist-watchorfinger/armcuff.Despite promising,these contact-based BP measurements have some shortcomings.First,their performance is highly dependent on the user's physical movements,ambient lighting conditions or even skin tattoos.Second,these systems need the user to wear particular devices or sensors,which may cause discomfort due to cuff


Contact-free BP measurement has been proposed recently leveraging on camera or wireless sensor [5],[6].The camerabased BP measurement utilizes the property of video/image data induced by pulse motions such as the pulse motions at fingertip [5].However,its performance relies heavily on illumination conditions and motion changes.A small change in light or movement may degrade accuracy dramatically.Wireless sensor-basedmethodsuseradiofrequencysignalstoacquireskin or blood vessel displacement caused by pulse wave transmission for BP measurement [6].Despite the progress achieved,these systems may not achieve accurate measurement as they cannot accurately capture tiny skin or vessel perturbations (i.e.,less than 1mm)due to low operating frequency and limited


Millimeter-wave (mmWave)sensing has been advocated as a plausible solution for contact-free BP measurement.The high frequency and large bandwidth of mmWave enable capturing tiny variations caused by pulse activities [7],[8].In particular,


1536-1233©2025IEEE.All rights reserved,including rights for text and data mining,and training of artificial intelligence and similar technologies.Personal use is permitted,but republication/redistribution requires IEEE permission.See https://www.ieee.org/publications/rights/index.html for more


d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap


pply


<footer>Received 22January 2025;revised 18June 2025;accepted 24July 2025.
Date of publication 31July 2025;date of current version 3December 2025.Recommended for acceptance by W.Gong.(Corresponding author:Tao Gu.)This work involved human subjects or animals in its research.Approval of all ethical and experimental procedures and protocols was granted by the Science &Engineering Subcommittee,Macquarie University under Application No.520221141241381,and performed in line with the National Statement on Ethical Conduct in Human Research 2007.
Zhenguo Shi is with the School of Computer Science and Engineering,University of New South Wales,Sydney 2052,Australia (e-mail:shizhenguotvt @gmail.com).
Tao Gu,Yu Zhang,and Xi Zhang are with the School of Computing,Macquarie University,Sydney 2109,Australia (e-mail:tao.gu@mq.edu.au;y.zhang@mq.edu.au;zaibuer@gmail.com).
Digital Object Identifier 1536-1233©2025IEEE.All rights reserved,including rights for text and data mining,and training of artificial intelligence and similar technologies.Personal use is permitted,but republication/redistribution requires IEEE permission.See https://www.ieee.org/publications/rights/index.html for more d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
<header>P+:CONTACT-FREE BLOOD PRESSURE MEASUREMENT USING MILLIMETER- 519</header>


SHI et al.:MMBP


WAVE RADAR


519


with mmWave signal reflection received at the receiver side,one can obtain the skin displacement.Since skin displacement is caused by pulse motions,the characteristics of pulse movements can be effectively captured and used for BP measurement [8].However,applying mmWave sensing for contact-free BP measurement is not a trivial task and several fundamental challenges remain to be addressed,which we summarize as


Challenge 1:Achieving accurate BP estimation using mmWave-based systems becomes significantly challenging as the measurement distance increases.In such systems,mmWave radar captures raw reflections to represent the subtle skin displacements caused by pulse wave activities.However,the high frequency and short wavelength of mmWave signals make them inherently susceptible to noise,particularly in the time domain.As the distance between the radar and the target increases,environmental interference and background noise become more pronounced [9],burying the clean pulse signals under a noise floor.Thus,it is extremely hard to extract useful features from these signals for BP measurement,leading to poor performance.Therefore,ensuring reliable BP estimations at increased distances is a critical issue in mmWave-based BP


Many efforts have been made to mitigate the impact of noise on the desired pulse signals,while most of them are under the condition of short-measurement distance.Among these,matrix factorization techniques,e.g.,Non-Negative Matrix Factorization (NMF)[10],have been widely utilized for noise reduction in thetimedomainbyisolatingcleansignalsfromnoisethroughthe properties of the signal matrix.However,their implementation is highly complex and involves a slow convergence process.Principal component analysis (PCA)is another time-domain based method that typically chooses a certain group of principal components for signal reconstruction and noise reduction [11].Despite its effectiveness,selecting appropriate principal components can be challenging.Apart from that,in the frequency domain,methods like the Butterworth filter have been explored,leveraging the frequency characteristics of the signal to filter out unwanted components [12].While this technique is simple to implement,its fixed cut-off frequencies limit its ability to adapt to varying noise conditions,resulting in suboptimal performance.Additionally,our preliminary study in [13]proposed a noise mitigation approach by leveraging signal property in delay-Doppler (DD)domain.This method effectively enhances pulse waveform quality by exploiting signal properties in the DD domain rather than time or frequency domains in the existing literature,offering effective noise


While the above methods can partially enhance signal patterns,they are generally effective only at short measurement distances,where the radar must be placed very close to the subject (e.g.,≤10cm),limiting practicality and convenience.Longer measurement distances are essential for improving user comfort and enabling more flexible applications.However,those methods often fail to reconstruct accurate pulse signals at longer distances due to increased noise and deteriorated signal quality,leaving a critical gap in addressing distance-induced


Challenge 2:Enabling reliable BP estimation with shortened measurement durations remains a significant challenge in mmWave-based systems,particularly when tiny motions occur


frequently.Small-scale or tiny motions,such as essential tremors and resting tremors,frequently occur unintentionally [14],[15].Even minor distance variations caused by tremors can significantly impact the performance of contact-free mmWave BP measurement [16].Such tiny motions interact nonlinearly with the desired signals,resulting in severe distortions in signal properties.This challenge becomes further pronounced when the measurement duration is shortened.Shorter durations result in less data being collected,which reduces the system's ability to differentiate clean pulse signals from motion-induced disturbances.Additionally,the limited data exacerbates the impact of residual noise and motion distortions,making it more difficult to reconstruct a reliable pulse waveform


Numerous efforts have been devoted for motion-reduction problems,predominantly assuming sufficient measurement duration.Signal decomposition algorithms (e.g.,Wavelet [17],Empirical Mode Decomposition (EMD)[18]and independent component analysis (ICA)[19])have been proposed to decompose the received signal into several sub-components to separate the interference caused by tiny motions and the clean signals.However,selecting optimal decomposition parameters is challenging,and residual motion continues to negatively affect clean signals [20].Moreover,deep learning techniques,such as deep contrastive learning and variational encoder-decoder networks [21],have been proposed to mitigate motion impact,while they are always constrained by their reliance on large training datasets and frequent re-training,limiting real-world applicability.Additionally,the nonlinear adaptive filter (NLAF)shows a potential to address nonlinear motion and has demonstrated its effectiveness in speech signal processing [22].However,its application in mmWave-based BP measurement is limited as it requires an actual pulse waveform as a reference,which is unavailable due to the absence of prior knowledge of noise or pulse signals.An attempt [23]to generate a reference signal using delayed information from received data achieved limited success,as high correlation between the artificial signal and raw pulse data reduced the effectiveness of motion


Despite promising,the aforementioned methods experience significant performance degradation when the measurement duration is insufficient.These approaches rely heavily on ample data to effectively separate signal components or train robust models,restricting their effectiveness under shorter durations.However,longer measurement duration would cause discomfort in users'experience and require more resources for data processing.Therefore,addressing motion-induced distortions within shortened measurement duration is essential to enhance the accuracy,usability,and practicality of these


To address the above challenges,in this work,we develop a novel contact-free mmWave-based system,termed mmBP+,to achieve accurate and robust BP measurement with long measurement distance and shortened measurement duration.In our previous version of mmBP [13],two major challenges have been addressed:noise reduction and motion compensation.Using Delay-Doppler Domain Feature Transformation (DDFT),mmBP effectively exploited signal properties in the DD domain to enhance pulse waveform quality,mitigating noise interference.Additionally,the temporal referential


d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap


<footer>d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
<header>IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20 520</header>


520


functional link adaptive filter (TR-FLAF)leveraged periodic and correlated properties of pulse signals to reduce the influence of tiny motions.While mmBP demonstrated reliable performance,itscapabilitieswereconstrainedbychallengessuchasincreasing measurement distances and shortened durations,limiting its practical


Building upon these limitations,mmBP+proposed in this work can achieve superior BP estimation accuracy and robustness under more diverse and challenging conditions.Toward that end,mmBP+incorporates Fractional Fourier-based DDFT (FrFDDFT)and Periodic Signal Feature-based FLAF (PSF-FLAF)to extend robustness and accuracy.FrF-DDFT enhances feature extraction by leveraging the Fractional Fourier domain to isolate pulse signals from residual noise induced by longer measurement distances.Unlike DDFT,FrF-DDFT better discriminates between pulse signals and noise sharing similar DD characteristics by exploiting additional representation differences in the fractional domain,significantly improving noise mitigation over extendedranges.OurexperimentsinSectionIIIdemonstratethat FrF-DDFT reduces the measurement error by approximately 30%for distances up to 40cm,which was not achievable with the earlier approach.Moreover,PSF-FLAF refines motion compensation by generating reliable reference signals using an exponentially weighted moving average (EWMA)approach.This enables PSF-FLAF to address dynamic and frequent tiny motions effectively,without relying on extended measurement durations,unlike TR-FLAF,which required temporal extensions to gather sufficient clean pulse signals.As shown in Section III,PSF-FLAF is able to maintain BP estimation accuracy at a minimum measurement duration of 10seconds,which is critical for user comfort and practical deployment.Additionally,we expanded the experimental scope significantly in this work.We evaluated the system under diverse conditions,including varying distances,tiny motion conditions,and durations,providing a comprehensive validation.This addresses the scalability and robustness concerns not covered in the prior conference paper,pushing the system closer to real-world


In summary,the key contributions of this paper are summarized as follows.r


r
We propose a novel BP measurement system leveraging on mmWave signal characteristics and representative features in the delay-Doppler-fractional Fourier (DDF)domain.mmBP+is fully contact-free and does not require wearing any devices.mmBP+is capable of achieving high accuracy and being robust to various measurement distances and durations.Hence it is highly promising for real-world deployment.
r


r To address the measurement distance-sensitive challenge,we propose a novel fractional Fourier transform based DDFT (FrF-DDFT)to extract representative features from the delay-Doppler-fractional Fourier (DDF)domain for pulse waveform construction.FrF-DDFT can effectively reduce the noise caused by increased measurement distances and extract effective features for BP estimation,enhancing distance robustness and improving estimation accuracy.To the best of our knowledge,we are the first to leverage DDF domain features to estimate BP


IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20




Fig.1.Key processing steps in


r
To tackle the measurement duration-vulnerable problem,we propose a novel periodic signal feature based functional link adaptive filter (PSF-FLAF)to filter out the influence of tiny motion on mmWave reflections.In doing so,PSF-FLAF is able to enhance the desired signal and construct an accurate pulse waveform without prolonging the measurement duration,even in the case that tiny motions occur frequently.This can dramatically improve the BP estimation accuracy and user experience.
r
To evaluate the performance of mmBP+,we conduct more experiments under various conditions and parameters.Extensive results verify that the estimation errors of SBP and DBP meet the boundaries of AAMI with a distance of up to 40cm and a measure duration of at least 10


# II.DESIGN OF MMBP+


This section describes our mmBP+design.As illustrated in Fig.1,mmBP+estimates BP values through four main steps:mmWave Reflection Capturing,Noise Mitigation,Motion Compensation,and BP Estimation.We begin by providing an overview of mmBP+before delving into the specifics of each


mmWave Reflection Capturing:This step intends to collect the arterial pulse signal based on received mmWave reflections.The mmWave signal is able to accurately reflect skin displacements resulting from pulse motions because of its high frequency and broad bandwidth,which is critical for constructing pulse waveforms.As pulse waveform involves sufficient BP-related information,it can be utilized to estimate BP


Noise Mitigation:This step transforms the pulse signal acquired in the first step from the time domain to the DDF domain.This transformation takes advantage of the fact that the desired pulse signals and noise have distinct DDF responses.By separating them in the DDF domain,the desired signals can be preserved while the influence of noise is minimized.This improves the construction of the pulse


d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap


pply


<footer>d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
<header>MBP+:CONTACT-FREE BLOOD PRESSURE MEASUREMENT USING MILLIMETE 521</header>


SHI et al.:MM


MBP+:CONTACT-FREE BLOOD PRESSURE MEASUREMENT USING MILLIMETE


ER-WAVE RADAR


521


Motion Compensation:This step aims to mitigate the effects of tiny motions on the construction of the pulse waveform.To achieve this,we propose a periodic signal feature-based functional link adaptive filter (PSF-FLAF)to eliminate the nonlinear influence induced by tiny motions.In particular,we propose a periodicsignalfeaturesgeneration(PSFG)algorithmtogenerate an effective reference signal for the adaptive filter,resulting in improved pulse waveform construction.


BP Estimation:In the final step,six representative features in the DDF domain are extracted,which can effectively reflect the characteristics of BP activities.Then,these features are fed into a regression model to accomplish a successful BP measurement,by establishing an effective relationship between the BP values and features obtained.


# A.mmWave Reflection Capturing


The objective of this step is to extract pulse-related information based on mmWave reflections.To achieve this,we employ a commercially available mmWave radar,i.e.,TI IWR1843BOOST,which emits FMCW signals towards the subject's wrist and captures the reflected signals.Subsequently,the pulse waveform can be extracted from these reflections.We let x(t)depict the transmitted FMCW signal,which can be written as


$$x(t)=A_{T}e^{j\left(2\pi f_{c}t+\pi\frac{B}{T}t^{2}\right)},$$





where $A_{T}$denotes the amplitude of the transmitted signal, $f_{c}$represents the central frequency,B stands for the system bandwidth,and T is the chirp period.Then,we can obtain the received signal by


$$y(t)=A_{R}e^{j\left(2\pi f_{c}\left(t-t_{d}\right)+\pi\frac{B}{T}\left(t-t_{d}\right)^{2}\right)},$$





where td depicts the delay between the transmitted signal and the received signal,and $A_{R}$refers to the amplitude of the received signal.The value of AR is dependent on both the reflected energy of the skin surface and the distance between the mmWave radar and the skin surface of the subject's wrist.The beat signal s(t)that involves the pulse information can be achieved by mixing $x(t)$and $y(t)$,which is


$$\begin{aligned}{s(t)}&{{}=x(t)y(t)\approx A(t)e^{j(2\pi f_{d}(t)t+\phi(t))},}\\ {A(t)}&{{}=A_{T}(t)A_{R}(t),f_{d}(t)=\frac{2B d(t)}{c T},\phi(t)=\frac{4\pi d(t)}{\lambda},}\\ \end{aligned}$$





where $A(t),\:f_{d}(t)$and $\phi(t)$stand for the amplitude,frequency and phase of the beat signal,respectively.d(t)depicts the distance between the mmWave radar and the skin surface of wrist.c denotes the speed of light.λ represents the wavelength of mmWave signal.


Variations in the pulse cause the skin surface to displace,resulting in alterations in d(t).It is important to note that while all elements of s(t)(i.e., $A(t),f_{d}(t)$and φ(t))can be utilized to extract the pulse waveform,phase information φ(t)is more appropriate for detecting small-scale vibrations [7].Consequently,this paper regards φ(t)as source signal extract pulse characteristics for BP estimation.


# B.Noise Mitigation


Despite the fact that the phase signal φ(t)can indicate skin displacement resulting from pulse movements,it is exceedingly difficult to employ φ(t)directly for measuring BP values.The reason behind is that phase signal φ(t)acquired is frequently corrupted by environmental noise.This leads to a low signalto-noise ratio (SNR),which means that the pulse waveform is dominated by noise.As reported in [13],although signal processing techniques can enhance the time-domain phase signal's quality to some extent,the enhancement may be inadequate for fine-grained pulse waveform construction.Thus,constructing a comprehensive pulse waveform using time-domain signals is exceptionally challenging.


To overcome the above challenge,the previous mmBP system[13]introducedanoisemitigationalgorithmthatutilizedDD domain features to suppress noise and enhance pulse waveform quality.However,as a first attempt,the effective measurement distance of mmBP is very small (e.g.,a few centimetres).When the measurement distance increases,the residual noise becomes much more severer and is not negligible,which results in low SNR conditions and degrades BP measurement performance.This would considerably restrict the capability of mmBP in practical applications.To address these shortcomings,mmBP+in this work introduces a fractional Fourier transform-based DDFT (FrF-DDFT)designed to address noise challenges in longer measurement distances.By leveraging the unique properties of the fractional Fourier domain,FrF-DDFT effectively isolates pulse signals from noise,even when their characteristics overlap in the delay-Doppler domain.This innovation allows mmBP+to achieve reliable feature extraction and accurate BP measurements over extended distances,greatly enhancing its applicability and robustness for real-world use.To achieve this,we separate residual noise and the desired pulse signals by exploiting their characteristics in the fractional Fourier (FrF)domain.


Let ζ stand for the phase noise in the time-domain,which is modelled as an additive white Gaussian noise (AWGN)with zero mean and variance $\sigma_{\zeta}^{2}$.Thus,the received phase signal φ(t)can be expressed as


$$\phi(t)=\phi_{p}(t)+\zeta(t),$$





where φp(t)denotes the actual phase signal.Let Ps be the power of φp,then SNR in the time-domain is defined as $\textstyle\widehat{S N R}_{T}=\frac{P_{s}}{\sigma_{\zeta}^{2}}$.


$\phi_{p}(t)$


Given the above time-domain signals,the DD domain pulse data can be extracted via the following two steps.First,we perform the Wigner transform operation to map φ(t)from the time domain to the time-frequency (TF)domain,which can be expressed as


$$R[n,m]=\int g^{*}(t-n T)\phi(t)e^{-j2\pi m\Delta f(t-n T)}d t,$$





where $g(t-n T)e^{-j2\pi m\Delta f(t-n T)}$stands for the receiving filter
which aims to sample $R[n,m]$from $\phi(t).\;n\in\{0,\ldots,N-1\}$and $m\in\{0,\ldots,M-1\}$denote time and frequency indices,respectively.


d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap


<footer>d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
<header>IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20 522</header>


522


In the next step, $R[n,m]$is converted into the DD domain signal, $\Lambda[k,l]$,using symplectic finite Fourier transform (SFFT)[24],which is


$$\Lambda\left[k,l\right]=\frac{1}{\sqrt{N M}}\sum_{n=0}^{N-1}\sum_{m=0}^{M-1}R\left[n,m\right]e^{-j2\pi\left(\frac{k n}{N}-\frac{l m}{M}\right)},$$





where k ∈{0,...,K −1}and l ∈{0,...,L −1}stand for Doppler and delay indices,respectively.It is noted that,the pulse signals and noise have different DD properties,so they are mainly distributed in different resource grids in the DD domain.Inthis regard,it is possibletoseparatepulseinformation and the interfering data.Notably,although this operation can reduce noise to a great extent,it is difficult to eliminate the noise data that has similar DD domain characteristics with the pulse signals,hence,the residual noise still exists.Specifically,we select the row of Λ whose Doppler shift matches that of the pulse waveform and use it as DD-domain feature signal for further processing.Let r denote the selected DD-domain feature signal,which can be expressed as r =� $r=\widehat{\phi_{p}}+\widehat{\zeta},$where $\widehat{\phi_{p}}$stands for the selected phase signal in DD-domain and its power �Ps is approximate to $P_{s}.\tilde{\zeta}$represents the residual noise of the selected row,which has the same Doppler shift with the selected signals,and it follows the AWGN distribution with zero mean and variance $\widetilde{\sigma_{\zeta}}^{2}$.In this regard,SNR of the selected row is defined as $\begin array}{l}{\mathrm{S N R}_{D D}=\frac{\widehat{P_{s}}}{\widehat{\sigma_{\zeta}}^{2}}}\\ \end{array}$.When the measurement distance
is short,the residual noise �ζ is quite small and negligible.Moreover,�Ps is close to Ps and �σζ 2
is much smaller than σ2ζ,
so SNRDD is much larger than SNRT =Ps
σ2
ζ
.Consequently,
the impact of noise on pulse waveform construction can be effectively reduced,achieving fine-grained DD-domain feature signals.However,this conclusion may not hold anymore when increasing the measurement distance.The reason is that a longer measurement distance would induce more residual noise involved in the selected feature signals.Since the residual noise andselectedfeaturesignalsharethesameDDdomainproperties,it is challenging to distinguish them in the DD domain.As a result,there is a dramatic increase in residual noise power $\widetilde{\sigma_{\zeta}}^{2}$and a decrease in desired signal power $\widehat{P}_{s}$.This leads to much lower SNR conditions,SNRDD,thereby resulting in a dramatic performance drop in BP estimation.


$k\in\{0,\ldots,K-1\}$


$l\in\{0,\ldots,L-1\}$


$r$


$\widehat{\zeta}$


$\widetilde{\sigma_{\zeta}}^{2}$


$P_{s}$


$\textstyle\operatorname{S N R}_{T}=\frac{P_{s}}{\sigma_{\zeta}^{2}}$


$\mathrm{S N R}_{D D}$


To address the above problem,we propose to apply FrF transform to effectively eliminate the residual noise caused by long measurement distance and extract reliable features for BP estimation.The FrF transform is a generalization of the Fourier transform,which can map signals into the FrF domain.By applying FrF transform in (7),we can transform signals from TF domain into the delay-Doppler-fractional Fourier (DDF)domain.Although the residual noise has similar Doppler characters with pulse signals,they may have different representations in FrF domain.Therefore,it is easy to eliminate the residual noise from the selected signals based on their FrF domain properties.To be specific,we apply the proposed fractional symplectic finite


IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20


Fourier transform (FSSFT)in (7),which can be expressed as


$$\Lambda^{\beta,\rho}\left[k,l\right]=\frac{1}{\sqrt{N M}}\sum_{n=0}^{N-1}\sum_{m=0}^{M-1}R\left[n,m\right]\Psi^{\beta}(n,k)\Psi^{\rho}(m,l),$$





where $\Lambda^{\beta,\rho}[k,l]$stands for the DD domain signal with fractional angles order $\beta$and ρ. $\Psi^{\beta}(n,k)$and $\Psi^{\rho}(m,l)$are transform kernels,given as


$$\begin{aligned}{}&{{}\Psi^{\beta}(n,k)=A^{\beta}e^{j\frac{\operatorname{c o t}\beta}{2}(n^{2}\Delta t_{\beta}^{2}+k^{2}\Delta u_{\beta}^{2})e^{-j\frac{2\pi n k}{N}}},}\\ {}&{{}\Psi^{\rho}(m,l)=A^{\rho}e^{j\frac{\operatorname{c o t}\rho}{2}(m^{2}\Delta t_{\rho}^{2}+l^{2}\Delta u_{\rho}^{2})e^{-j\frac{2\pi n l}{M}}},}\\ \end{aligned}$$





where $A^{\beta}=\sqrt{\operatorname{s i n}\beta-j\operatorname{c o s}\beta}$and $A^{\rho}=\sqrt{\operatorname{s i n}\rho-j\operatorname{c o s}\rho}$.Δtβ,Δuβ and Δtρ, $\Delta t_{\rho}$stand for the sampling intervals for $R[n,m]$and $\Lambda^{\beta,\rho}[k,l]$in two directions,respectively.


To effectively minimize the residual noise,we first select the elements in $\Lambda^{\beta,\rho}$whose Doppler shift matches that of the pulse waveform,obtaining $r^{\beta,\rho}.$Then,we analyze the energy distribution in the FrF domain.It is worth noting that the pulse signals and residual noise have different representations in the FrF domain.Specifically,the desired signals are mainly concentrated with certain fractional angle orders $\beta$and ρ,while the residual noise is more diffuse.By selectively isolating signals in the FrF domain with the maximum energy,we can obtain a fine-grained pulse waveform,given as


$$r^{*}[l]=\mathop\\*{m aoperatorname}{__operatorname{{\beta\in[0,\frac\pi2]}}}_{\rho\in[0,\frac\pi2]}\mathcal{(}r^{\beta,\rho}[l])$$





where $\mathcal{P}(.)$power function.r∗stands for DDF domain feature vector under a certain Doppler shift and specific fractional angle orders that maximize the signal power.l is the time delay index.Following the above steps,the pulse information and the residual noise can be easily separated,bringing two major attractive advantages.First,the variation of the pulse signal is significantly enhanced,which is beneficial for fine-grained pulse representation.Second,residual noise caused by long measurement distances can be considerably alleviated,improving its capability for the case with long measurement distances.


# C.Motion Compensation


In practice,the accuracy of BP estimation can be adversely affected by tiny motions that occur naturally and unconsciously in the subject,such as hand tremors.Such tiny motions may be inevitable and more prevalent in certain populations,e.g.,elderly people or those with chronic medical conditions.As is shown in Fig.3(a),the presence of tiny motions would cause nonlinear interference to pulse signals.This makes it challenging to construct accurate pulse waveforms using these signals,degrading BP estimation performance.To address this issue,in this section,we present a periodic signal feature-based functional link adaptive filter (PSF-FLAF)to filter out the nonlinear impact caused by tiny motions to enhance the desired signal


d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap


pply


<footer>d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
<header>CONTACT-FREE BLOOD PRESSURE MEASUREMENT USING MILLIMETER-WA 523</header>


SHI et al.:MMBP+:


AVE RADAR




Fig.2.Structure of PSF-FLAF for motion compensation.




523




Fig.3.Performance of PSF-FLAF.


and construct an accurate pulse waveform.As demonstrated in Fig.2,the proposed PSF-FLAF is composed of three major modules:1)Periodic signal features generation (PSFG):generating reference signals c;2):Functional expansion block:enhancing the quality of reference signals c;3):Coefficient adaptation:filtering out interference contaminated by tiny motions.


1)Periodic Signal Features Generation:The proposed PSFFLAF is designed to clean the contaminated signals by leveraging on a functional link adaptive filter (FLAF).However,the performance of FLAF heavily relies on a reliable reference signal,which is not readily available due to the absence of prior information about noise or desired signals.In our previous mmBP system [13],the reference signal was generated from the original received mmWave signals.Despite progress,this approach was proved inadequate when tiny motions occurred frequently during the measurement period.To address this limitation,mmBP extends the measurement duration to capture uncontaminated signals,but this comes out with challenges such as increased processing requirements,higher system complexity,and discomfort for users.


To overcome these issues,in this work we propose a novel periodic signal feature generation (PSFG)scheme based on the exponentially weighted moving average (EWMA)algorithm.This PSFG scheme is able to effectively mitigate interference caused by tiny motions,preserve the periodic characteristics


Fig.4.Heatmap of correlation matrix Γ.


of pulse waveforms,and reduce the measurement duration.By doing so,it eliminates the need to extend measurement duration andenables thegenerationof areliablereferencesignal,evenunder conditions of frequent tiny motions during the measurement duration.Towards this end,we partition $r^{*}(n)$into two parts:periodic pulse waveforms and interference signals,expressed as


$$r^{*}(n)=\tilde{r}(n)+\mathcal{M}(n),$$





where $r$represents the uncontaminated periodic pulse waveform,whose overall tendency is relatively stable.M denotes the interference caused by tiny motions that change patternlessly.Given this,our proposed PSFG applies recursive operations to mitigate the impact of dynamic M on $r^{*}$,thereby obtaining an estimate of $\tilde{r}$with stable periodic features.Specifically,the recursive operation from the continuous delay index can be written as


$$\hat{r}(n)=\theta r^{*}(n)+(1-\theta)\hat{r}(n-1),$$





where ˆr(n)standsfortherecursiveoutputatthen-thdelayindex,which is also the estimated value of periodic pulse waveforms  ̃r.θ represents the forgetting factor and is set to be 0.1in this work.As illustrated in Fig.3(a)and (b),our PSFG can significantly reduce the impact of tiny motions on the pulse waveform even if the signal is contaminated by tiny motions over the whole measurement period.In other words,the periodic features of pulse waveforms are enhanced,contributing to reference signal generation.


Next,we will generate effective reference signals for FLAF based on the output of PSFG ˆr(n).As demonstrated in Fig.3(b),the overall trend of pulse morphology becomes patternless when residual tiny motions remain.In contrast,pulse morphology shows a stable tendency composed of periodic repeats when there are no residual tiny motions.To further analyze the impact of residual tiny motions on pulse waveforms,we present a heatmap of the correction matrix of ˆr(n)in Fig.4.The transition from blue to yellow indicates an increase in correlation from low tohigh.SegmentsAandBrefertothesituationswithoutandwith residual tiny motions,respectively.It is evident that segment A exhibits higher correlation values with other segments in


d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap


<footer>d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
<header>IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20 524</header>


524


comparison with segment B.This can be attributed to the fact that segments in the case without residual tiny motions display similar patterns,resulting in high correlation values.Conversely,segment B is impacted by residual tiny motions,thereby disrupting the correlation characteristic with other segments.


To generate reference signals,we divide DD-domain feature signal ˆr into I segments $c_{1},\ldots,c_{I}$.I is determined by two factors:the segment length and the overlapping region between adjacent segments.The segment length is established to be greater than one pulse period but less than two pulse periods in duration.This ensures that each segment captures the overall property of pulse morphology while minimizing complexity.The overlapping region facilitates the sharing of information betweensegments.Therefore,theeffectofI onBPmeasurement performance is contingent on the combined impact of segment length and overlapping region.In this work,we empirically set the values of segment length and overlapping region as 500ms and 100ms,respectively.


Then,we obtain the correlation matrix by


$$\Gamma(i,j)=\operatorname{c o r}(c_{i},c_{j}),$$





where cor(.)denotes the correlation operation.For the ith row of Γ,α(i)refers to the number of elements higher than a threshold.Notably,the threshold is dependent on system configuration,i.e.,the segment length and the overlapping region between adjacent segments.So,its value remains constant across different subjects.In this paper,we empirically set the threshold to 0.86.Then,the index with the largest value of α can be obtained by


$$I_{m a x}=\operatorname{a r g}\operatorname*{m a x}_{i\in[1,I]}(\alpha(i)).$$





Following the above steps, $c I_{m a x}$is determined as the reference signal.It is worth to note that the values of $I_{m a x}$and $c_{I_{m a x}}$change over time due to the differences in instant pulse representations.Therefore, $c_{I_{m a x}}$needs to be computed for each BP estimation.For simplicity,we use c to represent $c_{I_{m a x}}$in the remaining of this work.


2)Functional Expansion Block:The aim of the functional expansion block (FEB)is to improve the input signal's quality,and it consists of multiple functions that adhere to the universal approximation constraints [25].Different types of expansion models can be utilized,such as tensor,power series expansion,and trigonometric expansion.The trigonometric expansion is employed in this paper because of its computational efficiency and ability to provide a succinct representation of nonlinear functions [26].


At the nth iteration,the input vector c consists of K input samples c and can be represented as


$$\mathbf{c}=[c(n),c(n-1),\ldots,c(n-K+1)]^{T},$$





where c stands for the reference signal obtained in Section III-C1.


Based on this equation,the expanded input v(n)can be obtained with L elements according to trigonometric function expansion.Each element of $\mathbf{v}(n)$corresponds to input sample


IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20


$c(n)$,which can be written as


$$v_{j}(c(n))=\begin{cases}{c(n),}&{j=0}\\ {\operatorname{s i n}(q\pi c(n)),}&{j=2q-1}\\ {\operatorname{c o s}(q\pi c(n),}&{j=2q}\\ \end{cases}$$





where $q=1,2,\ldots,Q$denotes the expansion index,and Q depicts the expansion order. $j=0,1,\ldots,L-1$represents the functional link index.


3)Coefficient Adaptation:After obtaining v(n),this step moves to find out the coefficients of PSF-FLAF,w,which is defined as


$$\mathbf{w}(n)=[w_{0}(n),w_{1}(n),\ldots,w_{L-1}(n)]^{T}.$$





To approximate the nonlinear model,we minimize the error signal,e(n),by


$$e(n)=r(n)-g(n)=r(n)-\mathbf{w}^{T}(n)\mathbf{v}(n).$$





One way to obtain an appropriate coefficient vector w is to utilize adaptive methods that conform to the gradient descent rule [27].In this work,the adaptive method satisfying the stochastic gradient rule is employed to modify the filter coefficients.The weight is updated as


$$\mathbf{w}(n+1)=\mathbf{w}(n)+\frac{\eta\mathbf{v}(n)}{\mathbf{v}^{T}(n)\mathbf{w}(n)},$$





where η depicts the step size.Following the above rule,the coefficients of PSF-FLAF can be determined,and then we can usethePSF-FLAFtofilterouttheimpactcausedbytinymotions.


Fig.3(c)demonstrates the outcome of PSF-FLAF.It is clear that the influence of tiny motion on pulse waveform is notably diminished.In contrast to the contaminated signals shown in Fig.3(a),the variation pattern of pulse morphology in this figure is much more distinct.Consequently,the quality of pulse presentation is improved,which facilitates accurate BP measurement.


# D.Blood Pressure Estimation


At this stage,we apply well-established pulse waveform analysis techniques [28],[29]to extract key features from the signals in the DDF domain.Then,these extracted features are fed into the regression model for BP estimation.


1)DDF Domain Feature Extraction:We list the following six features that extracted from DDF domain pulse waveform.


Maximum peak (MP):MP refers to the highest point of a pulse signal in the DDF domain,corresponding to SBP.


First inflection point (FIP):FIP represents the first inflection point of a pulse waveform [30]in the DDF domain,which is associated with DBP.


Maximum to minimum ratio (MMR):MMR is calculated by dividing the maximum and minimum signal values of a pulse waveform in the DDF domain,which indicates the varying intensity of that pulse duration.


Maximum to inflection ratio (MIR):MIR is measured by taking the ratio of the maximum signal value to the signal value at the first inflection point of a pulse waveform [30]in the DDF domain,which is associated with arterial wave reflections.


Peak-to-peak interval (PPI):PPI is a metric that measures the peak-to-peak interval of the pulse waveform [31]in the


d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap


pply


<footer>d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
<header>MBP+:CONTACT-FREE BLOOD PRESSURE MEASUREMENT USING MILLIMETE 525</header>


SHI et al.:MM


MBP+:CONTACT-FREE BLOOD PRESSURE MEASUREMENT USING MILLIMETE


DDF domain,which provides a representation of the entire pulse waveform.


ER-WAVE RADAR


TABLE I CONFIGURATION OF MMWAVE RADAR


525


Expectation and variance:The expectation refers to the mean value of a pulse waveform,while the variance represents the degree of dispersion or variability from this mean.Both capture the statistical characteristics of pulse signals.


From the aforementioned information,these extracted features collectively provide a comprehensive representation of the pulse waveform's essential characteristics.These features are then processed through a machine learning-based regression model,establishing an effective mapping between pulse waveform characteristics and BP values with high accuracy and reliability.While incorporating additional features could potentially improve accuracy,it would significantly increase the complexity of the process.


2)Regression Method:Now,we use the regression model to output BP values using the features extracted from the previous step.To be specific,the regression model is trained to establish a strong correlation between the extracted features and BP values.Note that,linear regression models are inadequate in providing satisfactory results due to the nonlinear relationship between the extracted features and BP.As a result,only nonlinear regression models are considered in this study.


Several nonlinear models can be taken into account,e.g.,Support Vector Machine (SVM),Decision Tree (DT)and Random Forest (RF).In our conference paper [13],we demonstrated that mmBP with RF outperforms other regression models.Interested readers are referred to our conference paper for more details.In this work,mmBP+adopts RF as a regression model.Due to the limited space,we mainly present the results of RF.


# III.PERFORMANCE EVALUATION


The objective of this section is to assess mmBP+through extensive experiments under various settings and conditions.To be specific,we will firstly outline the system set-up and performance mstrics,i.e.,the AAMI standard [32]and the BHS standard [33].Then,we will validate the overall BP estimation accuracy of mmBP+followed by its robustness to measurement distance and duration.Additionally,we will examine the effectiveness of the key algorithms in mmBP+,and then provide comprehensive performance comparison of mmBP+against the existing related methods.


# A.Experimental Set-Up and Metrics


To implement mmBP+,a commercially available mmWave radar is employed,specifically the TI IWR1843BOOST that comprises of one transmitting (TX)antenna and four receiving (RX)antennas.Table I provides a comprehensive outline of the radar's configuration.To collect the raw mmWave signals,we utilize the TI DCA1000board,and these signals collected are then processed using a desktop PC with an i79750CPU and 16GB RAM.


All experiments are performed within a quiet environment,with a room temperature maintained between 20–22Celsius







$$\frac{\text}{R}\ \\ {\textcir{{\ }}\frac{\text{{(D C A l00E0M)}}}{{\ \text{{(})(}}}{\ \text\{{{(}}}1000E0M)}}\\ {\text{{(}}}end\\\{{\$$


Fig.5.Experiment setup to compare mmBP+with Omron device.


degrees.33individuals participated in our experiment,comprising of 15females and 18males,with weights ranging from 48to 91kg and ages between 23and 68years old.Of the total participants,17are aged between 23–40years old,while the remaining 16individuals are aged between 41–68years old.Among these participants,23were healthy individuals without any known medical conditions,while 8had clinically diagnosed hypertension.The Human Research Ethics Committee of our institute has granted approval for the data collection process in this study.Fig.5illustrates the experimental setup.The subject is instructed to sit on a chair with back support,make a fist,and place his/her wrist and hand on the desk,with his/her purlicue facing upwards.A mmWave radar is positioned on the desk,5cm above the subject's wrist.Moreover,during the experiment,the subject is not allowed to wear any wrist accessories,such as watches.During each data collection,the participant is instructed to remain still for 25s,and has a 10min rest between two collections.Data collection is performed on various days and at different times.We gathered a total of 100samples from each participant.An FDA-approved,arm-cuff BP estimation device (Omron HEM-7121[34])is adopted as the ground truth,and the subject wears the arm-cuff at the heart level to obtain accurate data.It is noteworthy that all the experiments are conducted based on the "subject-level split"with the leave-one-out cross-validation (LOOCV)method,each training fold comprised 3,200samples (32participants × 100samples),while the remaining 100samples from the held-out participant were used for testing.


To validate the effectiveness of mmBP+,we use two com-
mon metrics,i.e.,Mean Error (ME)and Standard Deviation of mean error (STD),which are μ =�J
j=1(� $\begin array}{l}{\mu=\frac{\sum_{j=1}^{J}(\hat{b_{j}}-b_{j})}{J},\sigma=}\\ \end{array}$��J $\sqrt{\frac{\sum_{j=1}^{J}(\widehat{b_{j}}-b_{j}-\mu)^{2}}{J}},$where μ,σ stands for ME and STD,


d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap


<footer>d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
<header>IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20 526</header>


526


IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20




Fig.6.LOOV performance for mmBP+system.


TABLE II PERFORMANCE COMPARISON WITH THE AAMI STANDARD





TABLE III PERFORMANCE COMPARISON WITH THE BHS STANDARD





respectively.�bj represents the estimate of BP values and $b_{j}$is the ground truth.J stands for the total number of samples.


# B.Overall Performance


To evaluate the effectiveness of mmBP+,as shown in Table II,we compare its estimation error against that of mmBP (i.e.,[13])and the acceptable error range set by the Association for the Advancement of Medical Instruments (AAMI)[32].The results indicated in this table demonstrate that mmBP+outperforms mmBP and the error boundaries regularized by AAMI for both SBP and DBP.1To further assess the estimation performance of mmBP+,in Table III,we then carry out another comparison of its accuracy against that of mmBP and the standards established by the British Hypertension Society (BHS)standard [33].As reported in Table III,both SBP and DBP estimations of mmBP+are superior to those achieved by mmBP and obtain a Grade A rating.


1Note that,AAMI is adopted as a metric to evaluate the estimation accuracy of mmBP+given the dataset acquired in this work




Fig.7.Performance of mmBP+with different measurement distances.


While the mean error (ME)is one important metric,we emphasize that standard deviation (STD)is equally critical in assessing system stability.Compared to mmBP,mmBP+achieves significantly lower STD values,demonstrating enhanced reliability under diverse conditions.Additionally,the system achieves a 5%improvement in cases with errors no greater than 5mmHg and 10mmHg,which are clinically meaningful thresholds.These advancements reflect not only higher accuracy but also improved robustness,which is crucial for ensuring consistent and reliable performance in practical applications.


The LOOV results shown in Fig.6demonstrate mmBP+'s consistent performance across all individual test subjects,with each fold representing a complete subject dataset.The system maintains stable estimation accuracy without significant performance fluctuations between different subjects,confirming its robustness in handling natural variations in blood pressure characteristics across diverse individuals.This subject-level validation approach highlights the system's reliability in real-world applications.


# C.Evaluation on Measurement Distance and Duration


It is widely recognized that the robustness of BP estimation is a critical factor for successful real-world deployment.Hence,in this section,we conduct comprehensive experiments to evaluate the robustness of mmBP+on measurement distance and duration.


1)Robustness on Measurement Distance:We compare the estimation results of mmBP+against mmBP when the measurement distance varies,as depicted in Fig 7.In this figure,mmBP+


d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap


pply


<footer>1Note that,AAMI is adopted as a metric to evaluate the estimation accuracy of mmBP+given the dataset acquired in this work d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
<header>P+:CONTACT-FREE BLOOD PRESSURE MEASUREMENT USING MILLIMETER- 527</header>


SHI et al.:MMBP




Fig.8.Performance of mmBP+with different measurement duration.


WAVE RADAR




527


and mmBP are trained using the dataset with a measurement distance of 5cm.The trained models are then applied for BP estimation with various measurement distances,i.e.,5cm,10cm,15cm,20cm,30cm,and40cm.Fromthisfigure,wecanobserve several key findings.First,mmBP+demonstrates much stronger robustness over mmBP for both SBP and DBP estimations for all the measurement distances considered.Second,the errors of both SBP and DBP estimations for mmBP+remain within the AAMI boundary when the distance is up to 40cm.By contrast,it is hard for mmBP to meet the error requirements standardized by AAMI when the measurement distance is longer than 20cm.The reason behind this observation is that mmBP+proposes a novel approach (i.e.,FrF-DDFT)to effectively mitigate the noise induced by the increased measurement distance (A further evaluation on the effectiveness of FrF-DDFT is demonstrated in Section III-D1).In conclusion,mmBP+is capable of achieving highly accurate BP estimations with various measurement distances,which is essential for practical applications.


Although the experimental setup may require the wrist to be positioned under the mmWave radar for now,the extended measurement distance allows for greater flexibility in the $\mathrm{p o}$-sitioning and height of the radar.This reduces the need for precise wrist alignment,making the system more practical for real-world scenarios.Furthermore,this improvement enables adaptability in diverse settings,such as clinics,homes,or workplaces,enhancing both usability and user comfort.These enhancements address the scalability challenges and demonstrate mmBP+'s potential for large-scale deployment in healthcare environments.


2)Robustness on Measurement Duration:In Fig.8,we validate the performance of mmBP+and mmBP with various measurement durations.As reported in this figure,prolonging measurement duration results in better SBP and DBP estimates for both mmBP+and mmBP due to more features extracted from a larger dataset received.Our results also indicate that the measurement error tends to plateau beyond a certain threshold.Moreover,mmBP+can meet the error boundaries of AAMI when the measurement duration is no less than $7\text{s f o r}$SBP and 10s for DBP,while it is difficult for mmBP to achieve.This is credited to the fact that mmBP+develops a novel method,i.e.,PSF-FLAF,to effectively compensate for the impact of tiny motions on BP measurement,resulting in improved BP estimation performance (Section III-D2shows a detailed performance evaluation of PSF-FLAF).It is worth noting that increasing measurement duration would require more computing resources for


Fig.9.Performance of SNR improvement with different methods.




Fig.10.Impact of noise reduction methods on BP measurement.


data processing and cause more discomfort to subjects.Therefore,mmBP+achieves more potential in practical deployment accounting measurement performance and user experience.


# D.Effectiveness of Key Algorithms in mmBP+


1)Effectiveness of FrF-DDFT:As per the previous discussion,increasing the measurement distance would induce much severer noise to the mmWave reflections,resulting in low SNR conditions and degrading BP estimation accuracy.To tackle this issue,we propose FrF-DDFT to effectively mitigate noise and retain the desired signals by leveraging the feature properties in the DDF domain.In this section,we validate FrF-DDFT from various aspects,e.g.,SNR improvement and BP measurement accuracy.


In Fig.9,we provide a comparison of the proposed FrFDDFT with three state-of-the-art noise mitigation approaches,i.e.,BW filter [12],PCA [11],and NMF [10],in terms of SNR enhancement.The results show that the SNR condition of DDFT is substantially better than the other three methods,indicating that DDFT outperforms them in SNR enhancement.The reason behind the superior performance of DDFT is its ability to explore pulse-related features in the DDF domain,which is different from the existing methods that use the time or frequency domain information.Given the significantly different characteristics of mmWave signals and noise in the DDF domain,it is feasible to distinguish the noise and desired signals,thereby mitigating noise and improving SNR conditions.


To further verify the performance of FrF-DDFT,we demonstrate its impact on BP estimation accuracy in Fig.10.As can be observed,FrF-DDFT achieves the smallest estimation error among all the methods considered,suggesting that FrF-DDFT has a significant impact on BP measurement.This improvement


d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap


<footer>d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
<header>IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20 528</header>


528




Fig.11.Impact of motion compensation methods on BP


can be attributed to the fact that FrF-DDFT mitigates noise in the DDF domain,contributing to better SNR and hence improving the estimation


2)Effectiveness of PSF-FLAF:We develop PSF-FLAF to mitigate the nonlinear impact inducted by tiny motions on mmWave signals and hence improve BP measurement results.In this section,we examine the performance of PSF-FLAF on estimation


Fig.11demonstrates the estimation error of PSF-FLAF in comparison to three other algorithms.The other three methods are treated as the baseline.Note,N/A means no motion compensation is applied.As depicted in this figure,the proposed PSF-FLAF obtains superior performance,as seen in the much lower ME and STD values for both SBP and DBP.By contrast,the errors of N/A,ICA [19]and NLFA [23]methods are considerably higher than our method.The reason behind this is the fact that our PSF-FLAF can generate high-quality reference signals for a non-linear adaptive filter even in the case that tiny motions frequently occur within the measurement duration.Thus,it is feasible to effectively filter out the influence of tiny motions from clean pulse-related data,without the requirement of prolonging measurement duration.Note that,the NLAF may not be directly applicable to mmWave-based BP estimation.This is because it needs actual pulse waveforms as a reference signal,but in mmWave-based BP measurement,the noise and pulse signals are not known in advance,making it difficult to obtain an accurate reference signal for the NLAF.Therefore,the proposed PFS-FLAF is a promising candidate for achieving reliable BP estimation results with tiny


3)Case Study:Signal Processing Pipeline and BP Prediction:To further demonstrate the effectiveness of mmBP+in handling noise and motion artifacts,we present a case study of a single subject,illustrating the signal processing pipeline from raw mmWave signal to final BP prediction.As shown in Fig.12(a),the raw signal is heavily contaminated by noise and motion artifacts,making it impossible to discern any clear pulse waveform.After applying the proposed FrF-DDFT for noise reduction,Fig.12(b)shows that a significant amount of noise is removed,and a faint pulse waveform becomes visible,though still obscured by motion interference.Finally,Fig.12(c)demonstrates the result after applying the PSF-FLAF for motion compensation.It is clear that the influence of tiny motion on the pulse waveform is notably diminished.In contrast to the contaminated signals in Fig.12(a),the variation pattern of pulse morphology in Fig.12(c)is much more distinct,significantly improving the quality of pulse representation.Based on the clean


IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20




Fig.12.Impact of signal processing


TABLE IV BP ESTIMATION ERRORS UNDER DIFFERENT WRIST ANGLE RANGES AND RADAR PLACEMENTS (DISTANCE =40CM)





pulse waveform in Fig.12(c),mmBP+predicts the BP values as SBP:125mmHg and DBP:85mmHg,which closely match the ground truth values (SBP:126mmHg,DBP:88mmHg),demonstrating the system's accuracy and robustness in realworld


4)Impact of Wrist Posture and Radar Placement:To assess the influence of wrist posture and radar alignment on mmBP+performance,we conducted controlled experiments at a fixed radar-to-wrist distance of 40cm under varying wrist angles and radar mounting configurations.Two typical deployment modes were tested:(1)vertical placement (radar suspended directly above the wrist),and (2)horizontal placement (radar mounted on the tabletop).For each setup,we grouped the wrist-to-radar angular deviations into three ranges to simulate typical posture variations observed in practical use:(a)small deviations <8◦,(b)moderate deviations between 8◦and 30◦,and (c)large deviations between 30◦and 45◦.Table IV reports the average SBP and DBP estimation errors under each condition.The results indicate that mmBP+maintains stable performance under small angular


d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap


pply


<footer>d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
<header>:CONTACT-FREE BLOOD PRESSURE MEASUREMENT USING MILLIMETER-WA 529</header>


SHI et al.:MMBP+:


AVE RADAR


TABLE V PERFORMANCE COMPARISON OF MMWAVE-BASED BP MEASUREMENTS





529


variations (<8◦),which are already considered in our main dataset.As angular deviation increases,BP estimation errors also rise,especially beyond 30◦.Overall,the vertical configuration yields lower errors compared with horizontal configuration.This performance variation is attributed to:(1)non-ideal antenna-wrist angular alignment affecting signal capture quality,and (2)compounded multi-path interference from both table surfaces and environmental reflections.While current horizontal placement shows slightly reduced accuracy,it offers distinct advantages for extended-range measurement applications.Our future research will focus on adaptive beamforming techniques and optimized antenna array designs to mitigate angular sensitivity and enhance system robustness across diverse deployment scenarios,including varying postures,environments,and user interactions.


# E.Comparison Against the State-of-the-Arts


In this section,we evaluate mmBP+by comparing it with four baseline systems–Blumio [7],SBPM [8],WaveBP [35]and AirBP [36]in respect of estimation errors,comfort level,calibration,motion robustness,measurement distance and measurement duration,using the reported results from each of these systems.


As presented in Table V,mmBP+outperforms the other four methods in the performance of estimation accuracy.To be specific,the SBP and DBP of mmBP+are 0.65mmHg and 1.31mmHg,respectively.These errors are considerably smaller than those of other approaches $\mathrm{(i.e.,}geq1.7$and ≥2.85for SBP and for DBP,respectively,in Blumio).In addition,mmBP+performs significantly better over other methods in respect of STD,e.g.,3.92mmHg and 3.99mmHg for SBP and DBP,respectively.By contrast,the best performance demonstrated in other methods (i.e.,in Blumio)are 5.59mmHg and 5.57mmHg for SBP and DBP,respectively.It is worth noting that Blumio requires calibration for BP measurement,making it a "user-dependent"method that may introduce additional processing complexity.Additionally,mmBP+exhibits high robustness against small-scale and tiny motions,which is crucial for practical applications.In contrast,the motion robustness of all the other methods remains questionable.


In addition to the limitations in accuracy and robustness,the above four existing schemes may still have other drawbacks.For instance,Blumio has stringent requirement of wearing a mmWave radar device on the wrist and securing it with a medical adhesive patch,which may not be practical or user-friendly for real-world applications.In addition,the need for calibration is


another concern that limits its potential for practical applications.In SBPM,no study has been reported for DBP,as this method is solely focused on SBP estimation.It should be noted that measuring DBP is also crucial for accurate BP measurement,and it is typically more difficult to measure compared to SBP.Furthermore,both AirBP and WaveBP propose deep learning-based methods,which,while promising,increase the reliance on more powerful hardware and raise concerns about the generalization ability of the networks across diverse user populations and environmental conditions.These factors may pose challenges for practical deployment.mmBP+introduces a new system design that achieves high accuracy in a completely contactless and calibration-free manner while gaining strong robustness to tiny motions.


# IV.DISCUSSION AND FUTURE WORK


Evaluation on clinic setting:mmBP+is capable of achieving successful BP estimation with high accuracy and strong robustness,based on the dataset acquired from 33subjects,normotensive and hypertensive cases.The results indicate mmBP+system is robust and capable of handling a wider range of physiological conditions,including hypertension.To further enhance the practicality of mmBP+,further evaluations will be conducted in clinical settings by including a wider range of health conditions (e.g.,Parkinson's disease),increasing the dataset size,and expanding the age groups.


Motion impact:The mmBP+system introduces an effective motion compensation approach (PSF-FLAF)to suppress the impact of small,involuntary motions on pulse waveform construction.While the current implementation assumes the subject remains generally stationary,our controlled experiments highlight that certain micro-movements,such as fist-clenching,only cause manageable artifacts (SBP error:3.6mmHg;DBP:4.4mmHg),whereas activities like keyboard typing lead to significant degradation (SBP:9.7mmHg;DBP:12.3mmHg)due to continuous disruption of signal continuity.Notably,larger displacement movements,such as posture shifts or sudden jerks,can overwhelm the system's signal processing pipeline and render thepulsesignal difficult torecover.Toaddress this limitation,we plan to integrate motion segmentation,multi-antenna spatial filtering,and beamforming in future versions to better isolate useful signals under dynamic conditions,enhancing mmBP+'s robustness in real-world settings.


Dataset and evaluation consistency:One practical challenge in evaluating and comparing mmWave-based BP estimation systems lies in the absence of a standardized public dataset.


d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap


<footer>d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
<header>IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20 530</header>


530


Unlike fields such as image or speech recognition,this domain lacks benchmark datasets due to the hardware-specific nature of mmWave sensing,as well as the diversity of underlying principles used by different systems.For example,SBPM [8]relies on signal amplitude variation,WaveBP [35]captures chest motion,and AirBP [36]requires beamformed inputs.As a result,designing a single dataset that meets all these technical requirements is not feasible.Given these constraints,current works (e.g.,[35])have widely adopted system-level comparisons based on published performance metrics such as AAMI and BHS criteria,combined with qualitative evaluations of robustness,usability,and measurement constraints.While this approach introduces inherent variability,it remains the most practical and informative method under current circumstances.Future efforts toward open datasets or simulation frameworks would greatly benefit standardized evaluation in this area.


Calibration and practical trade-offs:Although mmBP+is designedasacalibration-freesystemtoenhanceusabilityandfacil-itate deployment in real-world settings,the framework remains compatible with optional calibration mechanisms if required.For example,the motion compensation module (PSF-FLAF)can be initialized with user-specific pulse templates to better adapt to individual waveform patterns.Moreover,subject-specific samples can be incorporated during regression model training to improve accuracy.These strategies can enhance inter-session consistency and long-term stability,particularly in clinical or personalized monitoring scenarios.However,they also introduce increased complexity,user burden,and deployment constraints.Our current design represents a trade-off between accuracy and practicality,with the goal of achieving robust performance without calibration.Future work may explore lightweight or semi-automated calibration methods as optional extensions to further improve performance in demanding cases.


# V.RELATED WORK


In this section,we provide an comprehensive overview on the current BP measurement techniques,mainly outlining their characteristics and analyzing their respective advantages and disadvantages.


Cuff-based BP measurement has gained widespread acceptance as an effective non-invasive BP estimation approach.The basic principle is to measure SBP and DBP by inflating and deflating an inflatable cuff,which is wrapped around the subject's arm or finger.This method is commonly employed in clinical and home settings,using instruments such as traditional mercuryor electronicsphygmomanometers [37],[38].However,the inflation of the cuff during the measurement process may cause discomfort or even pain to the users.


Wearable BP measurement detects BP values by using wearable devices,such as wristwatches,which can offer continuous BP monitoring as long as the subject wears them [39],[40].A recent solution in [39]proposed a BP estimation scheme that utilizes ECG and PPG to detect the proximal and distal timing of blood flows,respectively.Another work in [40]employed an accelerometer to measure proximal timing and PPG for distal timing.Despite their potential,there are still several challenges


IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20


that need to be addressed.For instance,the performance of these methods is highly dependent on the precise placement of the device,as even minor deviations may result in significant degradation of the measurement accuracy.Additionally,PPG-based approaches are susceptible to interference caused by environmental factors or tattoos on the skin.


Video/Image based $B P$measurement has recently become increasingly popular.This method involves using cameras to acquire video/images,which are then processed to extract relevant features for BP measurement.Specifically,the light reaction,such as absorption and reflection,on the targeted region of the body can be utilized for BP estimation [41],[42].The authors in[41]proposedtomeasureBPvaluesbyleveragingonthevideo plethysmogram (VPG)collected from the palm of the subject's hand.By establishing an effective relationship between internal pressure and blood vessels using VPG,they achieve successful BP measurement.In another study [42],the authors collected VPG from the subject's cheek and utilized PTT and VPG for BP measurement.Although these methods have their advantages,they require strict adherence to lighting conditions and may raise privacy concerns due to the use of cameras.


RadiofrequencybasedBPmeasurementrealizeBPestimation by exploiting changes in radio frequency signals exerted by blood flow [43],[44].In [43],a contact-free BP estimation scheme was developed.The sensor system is positioned in front of the subject for ultra-wideband (UWB)signals collection and processing,extracting critical features relevant to BP estimation.With the same purpose,the authors in [44]designed a Doppler radar-based BP measurement system,which is positioned 0.5meters away from the subject to collect and process continuous wave (CW).While these systems enable contact-free BP measurement,their effectiveness may be limited in practice due to low frequency and narrow bandwidth.


mmWave based BP measurement has shown promise due to its wider bandwidth and higher frequency.By detecting small variations in physiological signals,such as pulse waveform,mmWave sensing can realize successful BP measurement through the extracted pulse information,which is typically less than 1mm in size.However,only a few studies have explored this direction.In[45],theauthorsperformedanexperimentalstudytoshowthat changes in mmWave signal power are related to variations in BP,but the specific relationship has yet to be investigated.Another workin[46],[47]focusedonfeasibilitystudyofmmWave-based BP measurement by extracting time-domain features.Although these solutions represent initial attempts to utilize the property of mmWave signals for BP measurement,they did not specify any particular measurement methods or report any measurement accuracy.With the similar goal,the authors in [8]explored the use of mmWave reflection to estimate SBP,but they overlooked the importance of DBP estimation,which is crucial for reliable BP measurement and is often more difficult to obtain.A mmWave wearable system was designed in [7],which involves wrapping a mmWave sensor on the subject's wrist to capture reflected mmWave signals for BP estimation.Nevertheless,placing the sensor on the wrist may result in discomfort.Another issue is that it may not be practical to require the subject to provide actual BP values for calibration in real-world applications.Two


d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap


pply


<footer>d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
<header>531</header>


notable systems,proposed in [35],[36],attempt to address these challenges using deep learning-based approaches.[36]utilizes mmWave sensing to recover pulse waveforms from wrist arteries and applies neural networks for BP estimation.While effective,this increases the reliance on more powerful hardware and limits its practicality due to sensitivity to motion and environmental noise.Similarly,[35]focuses on arterial blood pressure waveform (ABPW)monitoring using mmWave reflections from the chest.While achieving high accuracy and supporting detailed cardiac waveform analysis,it relies heavily on complex deep learning architectures,raising concerns about computational cost and generalization across diverse users.Furthermore,the current methods for measuring BP based on mmWave signals are always susceptible to ambient noise and small/tiny movements.Although signal processing methods such as filtering or signal decomposition can partly address this issue,residual noise and motion still persist in mmWave reflections,making pulse waveform construction


# VI.CONCLUSION


This work utilizes mmWave technology to accomplish BP estimation in a contact-free manner,by leveraging features in the DDFdomaintoenhancetheaccuracy,robustness,andcomfortof the measurement.We developed a novel approach that utilizes the characteristics of mmWave signals in the DDF domain to mitigate the impact of noise on pulse waveform construction.Moreover,we designed an innovative approach for compensating non-linear interference resulting from tiny movements,in which an efficient reference signal is generated by utilizing the periodic and correlation features of pulse signals.Extensive results demonstrate that mmBP+can accomplish successful BP measurement with highly accurate and strongly motion-robust performance.Therefore,mmBP+gains a great potential in a wide range of real-world BP measurement


# REFERENCES


[1]F.D.Fuchs and P.K.Whelton,"High blood pressure and cardiovascular disease,"Hypertension,vol.75,no.2,pp.285–292,2020.
[2]M.R.Rebesco et al.,"A comparison of non-invasive blood pressure measurement strategies with intra-arterial measurement,"Prehospital Disaster Med.,vol.35,no.5,pp.516–523,2020.
[3]F.Beutel,C.Van Hoof,X.Rottenberg,K.Reesink,and E.Hermeling,"Pulse arrival time segmentation into cardiac and vascular intervals–implications for pulse wave velocity and blood pressure estimation,"IEEE Trans.Biomed.Eng.,vol.68,no.9,pp.2810–2820,Sep.2021.
[4]F.Schrumpf et al.,"Assessment of non-invasive blood pressure prediction from PPG and RPPG signals using deep learning,"Sensors,vol.21,no.18,2021,Art.no.6022.
[5]E.J.Wang et al.,"Seismo:Blood pressure monitoring using built-in smartphone accelerometer and camera,"in Proc.Conf.Hum.Factors Comput.Syst.,New York,NY,USA,2018,pp.1–9.
[6]D.Buxi,J.-M.Redouté,and M.R.Yuce,"Blood pressure estimation using pulse transit time from bioimpedance and continuous wave radar,"IEEE Trans.Biomed.Eng.,vol.64,no.4,pp.917–927,Apr.2017.
[7]C.Liao,O.Shay,E.Gomes,and N.Bikhchandani,"Noninvasive continuous blood pressure measurement with wearable millimeter wave device,"in Proc.IEEE 17th Int.Conf.Wearable Implantable Body Sensor Netw.,2021,pp.1–5.
[8]J.Shi and K.Lee,"Systolic blood pressure measurement algorithm with mmWave radar sensor,"KSII Trans.Internet Inf.Syst.,vol.16,no.4,pp.1209–1223,


531


[9]C.Shraddha,M.Chayadevi,and M.Anusuya,"Noise cancellation and noise reduction techniques:A review,"in Proc.1st Int.Conf.Adv.Inf.Technol.,2019,pp.159–166.
[10]T.Wang,F.Yang,and J.Yang,"Convolutive transfer function-based multichannel nonnegative matrix factorization for overdetermined blind source separation,"IEEE/ACM Trans.Audio,Speech,Lang.Process.,vol.30,pp.802–815,2022.
[11]Z.Zhang,G.Zhu,R.Wang,V.K.N.Lau,and K.Huang,"Turning channel noise into an accelerator for over-the-air principal component analysis,"IEEE Trans.Wireless Commun.,vol.21,no.10,pp.7926–7941,Oct.2022.
[12]F.A.Alturki,M.Aljalal,A.M.Abdurraqeeb,K.Alsharabi,and A.A.Al-Shamma'a,"Common spatial pattern technique with EEG signals for diagnosis of autism and epilepsy disorders,"IEEE Access,vol.9,pp.24334–24349,2021.
[13]Z.Shi et al.,"mmBP:Contact-free millimetre-wave radar based approach to blood pressure measurement,"in Proc.20th ACM Conf.Embedded Networked Sensor Syst.,New York,NY,USA,2023,pp.667–681.
[14]H.H.Fernandez et al.,A Practical Approach to Movement Disorders:Diagnosis and Management.Berlin,Germany:Springer,2021.
[15]B.Thanvi,N.Lo,and T.Robinson,"Essential tremor-the most common movement disorder in older people,"Age Ageing,vol.35,no.4,pp.344–349,2006.
[16]J.E.Johnson,O.Shay,C.Kim,and C.Liao,"Wearable millimeterwave device for contactless measurement of arterial pulses,"IEEE Trans.Biomed.Circuits Syst.,vol.13,no.6,pp.1525–1534,Dec.2019.
[17]D.Perpetuini et al.,"A motion artifact correction procedure for fNIRS signals based on wavelet transform and infrared thermography video tracking,"Sensors,vol.21,no.15,2021,Art.no.5117.
[18]R.Ranjan,B.C.Sahana,andA.K.Bhandari,"Motionartifactssuppression from EEGsignalsusing an adaptive signal denoising method,"IEEE Trans.Instrum.Meas.,vol.71,2022,Art.no.4000410.
[19]J.Lee et al.,"Motion artifact reduction in wearable photoplethysmography based on multi-channel sensors with multiple wavelengths,"Sensors,vol.20,no.5,2020,Art.no.1493.
[20]K.Xu,X.Jiang,and W.Chen,"Photoplethysmography motion artifacts removal based on signal-noise interaction modeling utilizing envelope filtering and time-delay neural network,"IEEE Sensors J.,vol.20,no.7,pp.3732–3744,Apr.2020.
[21]Z.Chen et al.,"MoVi-FI:Motion-robust vital signs waveform recovery via deep interpreted RF sensing,"in Proc.27th Annu.Int.Conf.Mobile Comput.Netw.,New York,NY,USA,2021,pp.392–405.
[22]S.Malik,J.Wung,J.Atkins,and D.Naik,"Double-talk robust multichannel acoustic echo cancellation using least-squares MIMO adaptive filtering:Transversal,array,and lattice forms,"IEEE Trans.Signal Process.,vol.68,pp.4887–4902,2020.
[23]S.Koshita,M.Abe,andM.Kawamata,"Recentadvancesinvariabledigital filters,"Digit.Syst.,vol.1,pp.275–289,2018.
[24]R.Hadani et al.,"Orthogonal time frequency space modulation,"in Proc.2017IEEE Wireless Commun.Netw.Conf.,2017,pp.1–6.
[25]G.Cybenko,"Approximation by superpositions of a sigmoidal function,"Math.Control,Signals Syst.,vol.2,no.4,pp.303–314,1989.
[26]J.C.Patra and A.C.Kot,"Nonlinear dynamic system identification using Chebyshev functional link artificial neural networks,"IEEE Trans.Syst.,Man,Cybern.B.Cybern.,vol.32,no.4,pp.505–511,Aug.2002.
[27]K.S.Sin,AdaptiveFiltering,PredictionandControl.Callaghan,Australia:Univ.Newcastle,1981.
[28]A.R.Kavsao ̆glu,K.Polat,and M.R.Bozkurt,"A novel feature ranking algorithm for biometric recognition with PPG signals,"Comput.Biol.Med.,vol.49,pp.1–14,2014.
[29]X.-J.Hu et al.,"Pulse wave cycle features analysis of different blood pressuregradesintheelderly,"Evidence-BasedComplement.Altern.Med.,vol.2018,no.1,2018,Art.no.1976041.
[30]B.N.Li,M.C.Dong,and M.I.Vai,"On an automatic delineator for arterial blood pressure waveforms,"Biomed.Signal Process.Control,vol.5,no.1,pp.76–81,2010.
[31]M.A.Navakatikyan,C.J.Barrett,G.A.Head,J.H.Ricketts,and S.C.Malpas,"A real-time algorithm for the quantification of blood pressure waveforms,"IEEE Trans.Biomed.Eng.,vol.49,no.7,pp.662–670,Jul.2002.
[32]G.S.Stergiou et al.,"A universal standard for the validation of blood pressure measuring devices:Association for the advancement of medical instrumentation/European society of hypertension/international organization for standardization (AAMI/ESH/ISO)collaboration statement,"Hypertension,vol.71,no.3,pp.368–374,


pply


<footer>d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
<header>IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20 532</header>


532


[33]E.O'Brien et al.,"The British Hypertension Society protocol for the evaluation of blood pressure measuring devices,"J hypertens,vol.11,no.Suppl 2,pp.S43–S62,1993.
[34]"Omron,"2015.[Online].Available:https://www.omronhealthcare-ap.com/au/product/128-hem-7121
[35]Q.Hu et al.,"Contactless arterial blood pressure waveform monitoring with mmWave radar,"in Proc.ACM Interactive,Mobile,Wearable Ubiquitous Technol.,2024,vol.8,no.4,pp.1–29.
[36]Y.Liang et al.,"airBP:Monitor your blood pressure with millimeter-wave in the air,"ACM Trans.Internet Things,vol.4,no.4,pp.1–32,2023.
[37]J.Cheng et al.,"Prediction of arterial blood pressure waveforms from photoplethysmogram signals via fully convolutional neural networks,"Comput.Biol.Med.,vol.138,2021,Art.no.104877.
[38]A.Chakraborty,D.Goswami,J.Mukhopadhyay,and S.Chakrabarti,"Measurement of arterial blood pressure through single-site acquisition of photoplethysmograph signal,"IEEE Trans.Instrum.Meas.,vol.70,2021,Art.no.4000310.
[39]S.Thomas et al.,"BioWatch —A wrist watch based signal acquisition system for physiological signals including blood pressure,"in Proc.Annu.Int.Conf.IEEE Eng.Med.Biol.Soc.,2014,pp.2286–2289.
[40]A.M.Carek et al.,"SeismoWatch:Wearable cuffless blood pressure monitoring using pulse transit time,"in Proc.ACM Interact.Mob.Wearable Ubiquitous Technol.,Sep.2017,vol.1,no.3,pp.1–16,doi:10.1145/3130905.
[41]N.Sugita,T.Noro,M.Yoshizawa,K.Ichiji,S.Yamaki,and N.Homma,"Estimation of absolute blood pressure using video images captured at different heights from the heart,"in Proc.41st Annu.Int.Conf.IEEE Eng.Med.Biol.Soc.,2019,pp.4458–4461.
[42]N.Sugita,M.Yoshizawa,M.Abe,A.Tanaka,N.Homma,and T.Yambe,"Contactless technique for measuring blood-pressure variability from one region in video plethysmography,"Chin.J.Med.Biol.Eng.,vol.39,pp.76–85,Feb.2019.
[43]I.Kim and Y.A.Bhagat,"Towards development of a mobile RF Doppler sensor for continuous heart rate variability and blood pressure monitoring,"in Proc.38th Annu.Int.Conf.IEEE Eng.Med.Biol.Soc.,2016,pp.3390–3393.
[44]H.Zhao,X.Gu,H.Hong,Y.Li,X.Zhu,and C.Li,"Non-contact beat-tobeat blood pressure measurement using continuous wave Doppler radar,"in Proc.2018IEEE/MTT-S Int.Microw.Symp.,2018,pp.1413–1415.
[45]Y.Yamaoka,J.Liu,and S.Shimamoto,"Detections of pulse and blood pressure employing 5G millimeter wave signal,"in Proc.16th IEEE Annu.Consum.Commun.Netw.Conf.,2019,pp.1–2.
[46]R.Kawasaki and A.Kajiwara,"Continuous blood pressure estimation using millimeter wave radar,"in Proc.2022IEEE Radio Wireless Symp.,2022,pp.135–137.
[47]R.Kawasaki and A.Kajiwara,"Continuous blood pressure monitoring with MMW radar sensor,"IEICE Commun.Exp.,vol.10,no.12,pp.997–1002,




Zhenguo Shi (Member,IEEE)received the MS and PhD degrees from the Harbin Institute of Technology (HIT),China,in 2011and 2016,respectively,and the second PhD degree from the University of Technology Sydney,Australia,in 2022.He was a research associate and senior research associate with Macquarie University and Univerisity of New South Wale,Australia.He is currently a research fellow with the School of Computing,the Queensland University of Technology,Australia.His research interests include Wireless sensing,AI,IoT,EHealth,Cognitive radio,


Wireless sensing,AI,IoT,Interference alignment and wireless


IEEE TRANSACTIONS ON MOBILE COMPUTING,VOL.25,NO.1,JANUARY 20








Tao Gu (Fellow,IEEE)is currently a professor with Macquarie University,an IEEE Fellow,and an expert in the fields of Embedded/Edge AI,Mobile and Ubiquitous Computing,and the Internet of Things.His publications typically appear in conferences including MobiCom,SenSys,IPSN,UbiComp and INFOCOM.He was a leadership role in many conferences,including as General Co-Chair of MobiCom 2022and TPC Co-Chair of IoTDI 2021.Visit https://taogu.site/for more


Yu Zhang (Member,IEEE)received the PhD degree in computer science from RMIT University,Australia.He is currently a postdoctoral associate with the School of Computing,Macquarie University,Australia.His research interests include Cyber-physical Systems,Mobile Computing,Embedded/Edge AI,Drone Systems,and Internet of


Xi Zhang received the BS degree from the Haibin College of Computer Science,Beijing Jiaotong University,China in 2014,the MS degree from the Monash University of Information Technology,Australia in 2018,and the PhD degree of computer science from RMIT University,Australia in 2024.His research interests include Internet of Things,mobile computing,and machine


d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap


pply


<footer>d licensed use limited to:University of Electronic Science and Tech of China.Downloaded on March 25,2026at 07:01:50UTC from IEEE Xplore.Restrictions ap</footer>
