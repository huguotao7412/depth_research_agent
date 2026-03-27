<header>electronics MDPI</header>


electronics


MDPI


# Article Random Body Movement Removal Using Adaptive Motion Artifact Filtering in mmWave Radar-Based Neonatal Heartbeat Sensing


Shiguang Yang
1,2
,Xuerui Liang 3,Xiangwei Dang 4,Nanyi Jiang 1,2,Jiasheng Cao 1,2,Zhiyuan Zeng
1,2and Yanlei Li 1,2,*





# check for updates


Citation:Yang,S.;Liang,X.;Dang,X.;
Jiang,N.;Cao,J.;Zeng,Z.;Li,Y.
Random Body Movement Removal Using Adaptive Motion Artifact Filtering in mmWave Radar-Based Neonatal Heartbeat Sensing.
Electronics 2024,13,1471.https://


Academic Editors:Changzhi Li and Emanuele Cardillo


Received:1March 2024
Revised:9April 2024Accepted:11April 2024Published:12April 2024


CC ? BY


Copyright:©2024by the authors.Licensee MDPI,Basel,Switzerland.This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY)license (https://


1National Key Laboratory of Microwave Imaging Technology,Aerospace Information Research Institute,
Chinese Academy of Sciences,Beijing 100190,China;yangshiguang21@mails.ucas.ac.cn(S.Y.);
jiangnanyi18@mails.ucas.ac.cn(N.J.);caojiasheng23@mails.ucas.ac.cn(J.C.);
zengzhiyuan19@mails.ucas.ac.cn(Z.Z.)
2School of Electronic,Electrical and Communication Engineering,University of Chinese Academy of Sciences,Beijing 100049,China
3Department of Pediatrics,Peking University Third Hospital,Beijing 100191,China;1810301305@pku.edu.cn 4School of Information Science and Technology,North China University of Technology,Beijing 100144,China;002429@ncut.edu.cn
*Correspondence:


Abstract:In response to the pressing requirement for prompt and precise heart rate acquisition during neonatal resuscitation,an adaptive motion artifact filter (AMF)is proposed in this study,which is based on the continuous wavelet transform (CWT)approach and takes advantage of the gradual,time-based changes in heart rate.This method is intended to alleviate the pronounced interference induced by random body movement (RBM)on radar detection in neonates.The AMF analyzes the frequency components at different time points in the CWT results.It extracts spectral peaks from each time slice of the frequency spectrum and correlates them with neighboring peaks to identify the existing components in the signal,thereby reducing the impact of RBM and ultimately extracting the heartbeat component.The results demonstrate a reliable estimation of heart rates.In practical clinical settings,we performed measurements on multiple neonatal patients within a hospital environment.The results demonstrate that even with limited data,its accuracy in estimating the resting heart rate of newborns surpasses 97%,and during infant movement,its accuracy exceeds


Keywords:MIMO mmWave radar;contactless sensing;vital signs;random body movement removal;adaptive motion artifact filtering


# 1.Introduction


In different countries,approximately 3%to 27%of newborn deaths occur each year,with about three-quarters of these deaths happening within the first week after birth [1].The leading causes of neonatal mortality are prematurity,birth asphyxia,and failure to initiate breathing at birth.Reducing neonatal mortality holds significant importance for global development.Neonatal resuscitation plays a crucial role in lowering newborn mortality rates,and heart rate serves as a vital indicator for medical interventions during neonatal resuscitation.Slow or inaccurate detection of heart rate may lead to delayed essential interventions or inappropriate measures,potentially resulting in severe outcomes,the inadequate management of the neonate's condition,unsuccessful resuscitation,and ultimately neonatal mortality [2–4].For premature infants,their organs and systems are not fully developed,and their immune system function is compromised.Most newborns experience pulmonary complications,such as neonatal respiratory distress syndrome,recurrent episodes of apnea,and chronic lung injury.Consequently,these newborns require necessary respiratory and heart rate monitoring in the neonatal ward


Electronics 2024,13,


ittps://www.mdp1.com/journal/electronics


<footer>CC ? BY Electronics 2024,13, ittps://www.mdp1.com/journal/electronics</footer>
<header>Electronics 2024,13,1471 2of 20</header>


Electronics 2024,13,1471


2of 20


Existing contact-based methods for measuring heart rate in newborns primarily include auscultation,palpation,pulse oximetry,and electrocardiogram estimation.Pulse oximeters and electrocardiograms have a higher accuracy,but it takes 1–2min from the birth of the newborn to obtain data using these instruments,which may surpass the optimal resuscitation time [6].Auscultation and palpation are convenient and relatively fast but lack accuracy in measurement.Non-contact detection methods mainly include optical cameras,WiFi,and radar detection [7,8].In optical detection,using visible light for sensing is susceptible to interference from ambient light and is affected by dark environments,which can impact detection performance.Moreover,most optical flow calculation methods have poor noise resistance and require corresponding hardware support.Infrared-based detection is susceptible to environmental temperature influences [9,10].WiFi-based detection faces the challenge of having multiple signals in the same frequency band in the environment,making it susceptible to interference and affecting its measurement accuracy [11–13].In order to compensate for the limitations of the aforementioned sensors,radar technology has been widely adopted for vital sign detection in recent years due to its superior penetration capabilities and anti-interference features,enabling continuous monitoring throughout the day


The detection principle of life signals based on radar primarily involves detecting displacement changes caused by respiration and heartbeat.The shorter the wavelength of the electromagnetic wave,the larger the phase shift caused by small movements,making the system more sensitive.Using high-frequency MIMO mmWave radar enables a more accurate detection of cardiac motion [18,19].MIMO technology enhances the spatial resolution of the radar and allows for beamforming,which enables the precise targeting of the heart and spatial filtering to eliminate interference in the environment.The use of MIMO mmWave radar in vital sign monitoring systems has significant practical significance in medical diagnosis,nursing home supervision,driver fatigue detection,and other fields [20].However,even though previous proposed solutions based on mmWave radar have been tested in ideal conditions,there are still some research gaps and limitations.For example,the current methods have not considered special scenarios,such as non-healthy newborns in hospitals,whose heartbeat amplitudes are relatively weak and whose frequencies are much higher than those of adults [21–23].During detection,RBM in newborns has a substantial impact on the system's detection performance.Newborns have small bodies,and the movements of their limbs and head will impact the radar echo,resulting in an insufficient signal-to-noise ratio and a significant amount of interference in the phase information.Traditional methods struggle to accurately determine the respiratory rate and heart rate in such


Currently,scholars primarily employ two categories of methods to mitigate the influence of body motion on the extraction of vital signs.One approach is based on a physical model,utilizing multiple radar sensors to retrieve physiological signals through the correlation of signals between sensors.Gu et al.proposed a multi-sensor fusion system that employs a camera-assisted radar for random body motion cancellation (RBMC)[24].A regular camera is used to measure body motion by tracking white dots on a small piece of black paper attached to the subject's shoulder.The phase information of the RBM,in the opposite phase,is added to the radar's demodulated signal to eliminate the effects of the RBM.This method has certain limitations,such as the complexity of camera deployment.Li and Lin suggested using two Doppler radars to simultaneously measure the subject on the front and back to counteract the effects of RBM.With the successful calibration of the DC offset,the system can successfully recover the respiratory and cardiac components [25].Wang et al.proposed using wireless mutual injection locking (MIL)of two radars to counteract the influence of RBM on a subject [26].Yu et al.developed a Doppler radar array for two-dimensional non-contact vital sign detection using four radar sensors.It achieved the elimination of random body motion noise in the human plane [27].Zhang proposed a novel chest–abdomen joint cardiorespiratory signal method using two IR-UWB radars simultaneously to detect respiration and heart rate.Considering the signal overlap between
<header>Electronics 2024,13,1471 3of 20</header>


Electronics 2024,13,1471


3of 20


vital signs and motion artifacts,the received radar signals are processed with the empirical wavelet transform (EWT)to eliminate clutter and mitigate motion interference [28].This enabled non-contact heart rate


Another approach is the data-driven method,which utilizes a single radar to predict physiological signals under motion interference through data analyses and inference.This method typically processes the raw signals by filtering,decomposing,fitting,and matching them to obtain physiological signals.However,it cannot capture the true measurement values at each moment,resulting in potentially significant variations in accuracy across different subjects or conditions.Lv et al.introduced a matched filter to invert the respiratory and cardiac spectra completely hidden under broadband background noise caused by largescale body motion.However,this method requires accurate heartbeat and respiration templates,which are impractical in real-world applications [29].Tariq et al.employed wavelet algorithms for detecting heart rate in phase-modulated Doppler radar signals.The ability of the wavelet transform to preserve both time and frequency information is utilized to analyze the phase-modulated Doppler radar signal,giving information about changes in heartbeat over very small intervals of time.This method performs well in ideal environments [30].Mercuri et al.used CWT to identify the locations of artifacts and then applied a moving average filter to smooth these identified artifacts.They also utilized a discrete wavelet transform (DWT)to separate the heartbeat signal from the respiratory signal,thereby achieving accurate detection [31].However,this method encounters issues whereby successful detection is not achieved even after


In the current research,detecting heart rate signals in the presence of RBM remains a challenge.Existing studies indicate that the displacement changes on the chest surface caused by the motion of the heart and respiration are different from those caused by RBM,resulting in different radar echoes.The frequencies of respiration and heartbeats change continuously over time,while the frequency of RBM changes discontinuously over time.This fundamental distinction has inspired us to employ time–frequency analysis methods to process radar echoes and filter out the influence of RBM on heart rate


In this paper,the heartbeat signals were detected using MIMO mmWave radar,and an adaptive motion artifact filtering method based on the continuous slow temporal variations in heartbeat frequency was proposed,building upon the wavelet transform for separating vital signs.This method combines cardiovascular motion models,data knowledge,and graphical algorithms to explore RBM removal techniques.The contributions of this article are as follows:


(1)A novel method is proposed to enhance the quality of heartbeat measurements using MIMO mmWave radar in the presence of RBM;
(2)The non-continuous nature of RBM is leveraged to mitigate its impact on the calculation of respiration and heart rates;
(3)By analyzing the time–frequency information on the chest surface,the spectra of RBM and heartbeat are separated in the temporal domain,the continuously changing heartbeat spectra are extracted,and the influence of RBM is


This paper is organized as follows:Section 2provides a comprehensive overview of the principles behind non-contact heartbeat perception using MIMO mmWave radar.It includes a detailed analysis of the performance of other wavelet-based vital sign detection methods and an elaborate exposition of the proposed AMF method for calculating respiratory and heartbeat frequencies under non-stationary body states.In Section 3,vital sign detection experiments were conducted on three subjects to evaluate the performance of the proposed method.The experimental results are used to assess the effectiveness of our approach.Finally,a discussion and conclusion are presented to summarize our


# 2.Methodology


In this study,MIMO mmWave radar was employed for neonatal vital sign detection.MIMO mmWave radar offers high resolution in range,azimuth,and elevation angles,facilitating precise localization of the participant's chest and accurate sensing of chest
<header>Electronics 2024,13,1471 4of 20ection</header>


Electronics 2024,13,1471


4of 20ection


movements.Figure 1illustrates the fundamental principle of vital sign detection using
mmWave radar.The surface movements of the chest caused by neonatal cardiopulmonary activity modulate the radar echo signals,resulting in a micro-Doppler effect that can be further processed to extract heartbeat information.
ments.Figure 1illustrates the fundamental principle of vital sign detection using mmWave radar.The surface movements of the chest caused by neonatal cardiopulmonary activity modulate the radar echo signals,resulting in a micro-Doppler effect that can be further processed to extract heartbeat




Figure 1.The principle of non-contact vital sign detection using mmWave radar Figure 1.The principle of non-contact vital sign detection using mmWave


During this research,we encountered the challenge of imprecise frequency measure-
ment of heartbeat signals due to RBM.In practical detection scenarios,RBM in newborns overlaps with radar echoes generated by cardiac and pulmonary activities,thereby severely compromising the accuracy of heart rate detection.In response to this challenge,a signal processing architecture was formulated in this study to leverage the distinct features of RBM and cardiac–pulmonary activities.Our overarching aim was to mitigate the interference stemming from RBM.During this research,we encountered the challenge of imprecise frequency measure-
ment of heartbeat signals due to RBM.In practical detection scenarios,RBM in newborns overlaps with radar echoes generated by cardiac and pulmonary activities,thereby severely compromising the accuracy of heart rate detection.In response to this challenge,a signal processing architecture was formulated in this study to leverage the distinct features of RBM and cardiac–pulmonary activities.Our overarching aim was to mitigate the interference stemming from


The adaptive RBM filtering method based on wavelet transform is depicted in Figure
2.It depicts the key steps of the method proposed in this article.After acquiring echo data from the MIMO mmWave radar,multi-channel data are subjected to beamforming,and static clutter is removed to perceive the motion signal of the chest surface.The specific data processing method for Figure 2a is detailed in Section 2.1.After the raw data of the chest surface are obtained,the phase is calculated,and the influences of respiration and RBM are preliminarily filtered out.The result is a micro-motion signal mixed with respiration,heartbeat,and RBM;Figure 2b,c demonstrate the corresponding outcomes,which are elaborated in Section 2.2.CWT is applied to the micro-motion signals in Figure 2d to analyze the frequency components at each moment and the trends of each frequency component.Subsequently,the RBM is removed through the AMF method,and the heart rate variation curve is fitted,as shown in Figure 2e,with an explanation of the AMF method in Section 2.3.Figure 2f presents the final heart rate results.The adaptive RBM filtering method based on wavelet transform is depicted in Figure 2.
It depicts the key steps of the method proposed in this article.After acquiring echo data from the MIMO mmWave radar,multi-channel data are subjected to beamforming,and static clutter is removed to perceive the motion signal of the chest surface.The specific data processing method for Figure 2a is detailed in Section 2.1.After the raw data of the chest surface are obtained,the phase is calculated,and the influences of respiration and RBM are preliminarily filtered out.The result is a micro-motion signal mixed with respiration,heartbeat,and RBM;Figure 2b,c demonstrate the corresponding outcomes,which are elaborated in Section 2.2.CWT is applied to the micro-motion signals in Figure 2d to analyze the frequency components at each moment and the trends of each frequency component.Subsequently,the RBM is removed through the AMF method,and the heart rate variation curve is fitted,as shown in Figure 2e,with an explanation of the AMF method in Section 2.3.Figure 2f presents the final heart rate results.VIEW 5of 21




Figure 2.An overview of the heart rate extraction method by adaptive filtering of RBM.Figure 2.An overview of the heart rate extraction method by adaptive filtering of
<header>Electronics 2024,13,1471 5of 20</header>


Electronics 2024,13,1471


# 2.1.MIMO Millimeter Wave Radar Induction Technology


5of 20


The principle of non-contact heart rate signal sensing using radar is based on the detection of subtle movements on the chest surface caused by cardiac and pulmonary activities.In normal conditions,the heartbeat frequency of neonates ranges from 120to 180beats per minute (bpm).When the heartbeat falls below 100bpm,medical professionals need to closely observe the condition of the newborn to ensure timely resuscitation if necessary.


It is generally accepted that the amplitude of body surface vibrations caused by heartbeat motion is approximately 0.1–4mm,while the amplitude of body surface fluctuations caused by respiratory motion ranges from around 1mm to 12mm.RBM,on the other hand,can cause body surface activity,with an amplitude ranging from 0to 50mm.Radar echoes also contain various types of noise,including but not limited to static interference and external dynamic interference.Therefore,the key to successful vital sign detection using radar lies in effectively filtering out noise.Over a certain period of time,the frequencies of respiratory and heartbeat signals fluctuate around fixed values,while the amplitude of these vital signs remains relatively stable.Vital signs exhibit quasi-periodic characteristics.It can be said that the detection of vital signs is akin to detecting a slow-moving target undergoing reciprocal motion at a fixed position.


We consider respiratory and heartbeat signals as sinusoidal oscillations,distinguishing them based on their amplitude and frequency characteristics.Assuming the subject is relatively stationary with respect to the radar,we establish the following model:


$$R(t)=R_{0}+r_{1}\operatorname{s i n}(2\pi f_{1}t)+r_{2}\operatorname{s i n}(2\pi f_{2}t)$$





where $R_{0}$is the distance between the radar and the target subject, $r_{1}s i n(2\pi f_{1}t)$is the respiratory signal, $r_{2}s i n(2\pi f_{2}t)\;{s\;t h e}$heartbeat signal,r1and r2are the amplitudes of the respiratory and heartbeat signals,and f1and $f_{2}$are the frequencies of the respiratory and heartbeat oscillation.


The stepped-frequency continuous wave (SFCW)signal is emitted by an MIMO millimeter wave radar to monitor micro-movements on the chest surface and torso.The radar transmits signals in frames,and according to [32],the transmission frequency starts from the initial frequency f0and increases over time with intervals of pulse duration ∆t.The frequency increment $\Delta f$is added $K-1$times until reaching the cutoff frequency $f_{e}=f_{0}+(K-1)\Delta f.$.The transmitted signal within a frame can be represented as follows:


$$s_{T}(t)=\sum_{k=0}^{K-1}\operatorname{e x p}[j2\pi(f_{0}+k\Delta f)t]r e c t\left(\frac{t-k\Delta t-\Delta t/2}{\Delta t}\right)$$


where t represents the fast time,and K represents the number of pulses.





The received signal relative to the target,assuming the distance between the target and the radar is $R(\tau),$can be represented as follows:


$$s_{R}(t)=A{\cdot}s\bigg(t-\frac{2R(\tau)}{c}\bigg)$$





where A denotes the amplitude of the received signal,c is the speed of light,τ is the slow time,and $R(\tau)$represents the distance between the target and the radar,as well as the target's relative motion.


$$R(\tau)=R_{0}+\Delta R(\tau)$$





The radar echo is mixed with its corresponding carrier and down-converted to baseband.The down-converted signal for each frame is then subjected to inverse Fourier transform to achieve pulse compression [33],as shown in the following equation:
<header>Electronics 2024,13,1471 6of 20</header>


Electronics 2024,13,1471


$$S_{b}(f)=\frac{A}{K T}\cdot\operatorname{e x p}\left(\frac{j4\pi f_{0}R(\tau)}{c}\right)\cdot\operatorname{e x p}\left(\frac{j2\pi(K-1)}{K}\left(f-\frac{2K\Delta f R(\tau)}{c}\right)\right)\cdot s i n c\Bigg(T\Bigg(f-\frac{2K\Delta f R(\tau)}{c}\Bigg)\Bigg)$$


where $T$represents the repetition time of the pulse.


6of 20





In an MIMO mmWave radar system,assuming the presence of M transmitting antennas and N receiving antennas,the system can be treated as an $M\times N$matrix called the channel matrix H.Each antenna has the capability to independently transmit and receive signals.Considering the transmitting signal as $s_{T}=\left[s_{T_{1}},s_{T_{2}},\cdots,s_{T_{M}}\right]^{T}$and the receiving signal as $s_{R}=[s_{R_{1}},s_{R_{2}},\cdots,s_{R_{N}}]^{T}$,the following channel model can be formulated:


$$s_{R}=H s_{T}+n$$


where $n=\left[n_{1},n_{2},\cdots,n_{N}\right]^{T}$denotes the noise component.





An MIMO mmWave system utilizes a combination of a 2D antenna array and SFCW signal to scan the RF reflections in 3D space.The target's distance relative to the radar is determined using Equation (5),and digital beamforming (DBF)is employed to steer the antenna beams towards the target [34].θ and φ represent the target's elevation angle and azimuth angle,respectively.The DBF results are presented as follows:


$$S\big(\theta,\varphi\big)=\sum_{m=1}^{M}w_{m}e^{j\frac{2\pi}{\lambda}m d_{T}\operatorname{c o s}\theta}.cdot\\sum_{n=1}^{N}w_{n}e^{j\frac{2\pi}{\lambda}n d_{R}\operatorname{s i n}\theta\operatorname{c o s}\varphi}$$


# 2.2.The Impact of RBM





In current research,a prominent class of methods for RBM removal focuses on wavelet transform at the algorithmic level.These methods primarily encompass CWT for vital sign sensing using various wavelet bases,signal noise separation through wavelet decomposition (WD)for signals contaminated with interference,and adaptive noise filtering employing EWT.


The vibrations caused by cardiac and respiratory activities,as well as RBM,are reflected in the phase variations in radar echoes [35].


$$\Delta\phi_{b}=\frac{4\pi}{\lambda}\Delta R$$





By substituting Equation (1)into the previous equation,we can establish the relationship between the surface variations in the chest and the phase variations in radar echoes as follows:


$$\Delta\phi_{b}=\frac{4\pi}{\lambda}[r_{1}\operatorname{s i n}(2\pi f_{1}t)+r_{2}\operatorname{s i n}(2\pi f_{2}t)]$$





During the simulation,ideal respiratory and heartbeat signals are modeled using sinusoidal functions,while RBM is based on actual measurement results.Therefore,when RBM occurs in the human body,the micro-movements on the chest surface can be considered as the superposition of RBM and the ideal respiratory and heartbeat signals.


Sinusoidal waves combined with Gaussian noise were employed to simulate respiratory and heartbeat signals in the ideal posture of the human body.The respiratory rate was set at 40bpm with an amplitude of 10mm,while the heart rate was set at 128bpm with an amplitude of 3mm.The signal-to-noise ratio (SNR)between the respiratory and heartbeat signals and the Gaussian noise was 30dB,as shown in Figure 3a.Figure 3b illustrates the resulting micro-movements on the chest surface after adding RBM to the respiratory and heartbeat signals.
<header>Electronics 2024,13,1471 7of 20</header>


Electronics 2024,13,1471




7of 20


Figure 3.The simulated signal.(a)The respiratory and heartbeat signal.(b)The mixed signal com-
prising respiratory,heartbeat,and RBM components.
Figure 3.The simulated signal.(a)The respiratory and heartbeat signal.(b)The mixed signal comprising respiratory,heartbeat,and RBM components.


The wavelet transform,as a multi-resolution analysis method,provides different res-
olutions at various positions in the time–frequency plane for linear time–frequency analysis of non-stationary signals [36].The CWT of a square-integrable function ()s t is defined The wavelet transform,as a multi-resolution analysis method,provides different
resolutions at various positions in the time–frequency plane for linear time–frequency analysis of non-stationary signals [36].The CWT of a square-integrable function s(t)is defined as follows:


$$\begin{array}{r l}{W T_{s}\big(a,b\big)}&{=\frac{1}{\sqrt{a}}\int_{-\infty}^{\infty}s\big(t\big)\psi*\big(\frac{t-b}{a}\big)d t}\\ {}&{=\big\langle s\big(t\big),\psi_{a,b}\big(t\big)\big\rangle}\\ {s.t.\;a}&{>0}\\ \end{array}$$





s(t),yab(f)





.


$$\psi_{a,b}(t)=\frac{1}{\sqrt{a}}\psi(\frac{t-a}{b})$$





,
1
()()
a b
t a
t
b a
ψ ψ
−
=(11)
Equation (11)represents the wavelet basis function,where a is the scale factor and
b is the translation factor.The mother wavelet undergoes scaling and shifting to generate the daughter wavelets.The scaling factor controls the frequency of the daughter wavelets;higher scales correspond to lower frequencies and vice versa.The wavelet coefficients are obtained by convolving the daughter wavelets with the signal.To preserve energy at each 1
Equation (11)represents the wavelet basis function,where a is the scale factor and b
is the translation factor.The mother wavelet undergoes scaling and shifting to generate the daughter wavelets.The scaling factor controls the frequency of the daughter wavelets;higher scales correspond to lower frequencies and vice versa.The wavelet coefficients are obtained by convolving the daughter wavelets with the signal.To preserve energy at each scale,the convolution is multiplied by a factor of 1
√a [37].The wavelet transform has the
capability to accurately localize both the time and frequency dimensions,thus offering superior time resolution for fast events,such as cardiac activities,and significant frequency resolution for slower events,such as respiratory actions.


scale,the convolution is multiplied by a factor of a
[37].The wavelet transform has the
capability to accurately localize both the time and frequency dimensions,thus offering superior time resolution for fast events,such as cardiac activities,and significant frequency According to [38],the analysis of the phase difference signal is performed using the
Morlet wavelet basis.The Morlet wavelet basis excels in time and frequency localization,making it suitable for time–frequency analysis of oscillatory signals [39].The following equation represents the time-domain mathematical expression of the Morlet wavelet:


$$\psi(t)=\frac{1}{\sqrt{\pi f_{b}}}e^{j2\pi f_{c}t}e^{-\frac{t^{2}}{f_{b}}}$$ c e t





where fb represents the bandwidth of the Morlet wavelet,and fc denotes the central frequency.


The phase difference signal is analyzed using a Morlet wavelet with a bandwidth of 3and a central frequency of 3.The phase signal comprises components attributed to respiration,heartbeat,and RBM,with the amplitude of RBM progressively increasing from 0.The objective of the analysis is to investigate the influence of RBM on respiratory and heartbeat signals.The analysis results are depicted in Figure 4.For 2D time–frequency plot of the CWT,peak detection is obtained via spectral slices of each time point.The frequency
<header>Electronics 2024,13,1471 8of 20</header>


Electronics 2024,13,1471


8of 20


with the maximum spectral peak within the newborn heart rate range (80–180bpm)is taken as the heart rate value.Finally,the results are smoothed for further analysis.nal cannot be accurately identified when the magnitude of the RBM signal exceeds three times that of the respiratory and heartbeat signals.




Figure 4.Phase and the processing result.(a,b)The simulated time-domain signals with different magnitudes of RBM.(c,d)The wavelet transform results corresponding to the phase signals.Figure 4.Phase and the processing result.(a,b)The simulated time-domain signals with different magnitudes of RBM.(c,d)The wavelet transform results corresponding to the phase signals.


After the increase in noise magnitude,direct analysis using CWT and employing the strategy of extracting the maximum value can no longer effectively remove the RBM.The magnitude of variation in RBM significantly affects the detection of respiratory and heartbeat signals using CWT.Figure 4a illustrates changes in motion on the chest surface when the amplitude of RBM is twice the amplitude of the simulated respiratory and heartbeat signals.The corresponding wavelet transform results are shown in Figure 4c,indicating a stable and accurate estimation of heart rate without any abrupt changes.Figure 4b represents changes in motion on the chest surface when the amplitude of RBM is four times the amplitude of the simulated respiratory and heartbeat signals.The corresponding wavelet transform results are depicted in Figure 4d,demonstrating a significant impact of RBM on the results.The heart rate exhibits a sudden jump at 3s,and the maximum peak does not correspond to the true heart rate,resulting in inaccurate estimations.Through multiple experimental comparisons,it has been observed that the heart rate signal cannot be accurately identified when the magnitude of the RBM signal exceeds three times that of the respiratory and heartbeat signals.


After the increase in noise magnitude,direct analysis using CWT and employing the strategy of extracting the maximum value can no longer effectively remove the RBM.According to [31],the fact that there is a higher time resolution in high-frequency components and better frequency resolution in low-frequency components in wavelet transform is utilized to localize motion artifacts.The motion artifacts at the identified locations are then smoothed to attenuate the motion signal.Furthermore,the Meyer wavelet is employed for further signal decomposition.The decomposition level is 5.Upon obtaining the decomposed signals,the frequency of the heartbeat signal is ascertained through the application of the fast Fourier transform (FFT).The mathematical expression for the Meyer wavelet is


$$\psi_{j,k}(x)=2^{-j/2}\psi\big(2^{-j}x-k\big)$$





where j and k are arbitrary integers,and $\psi(x)$represents a smooth real bandlimited function.


The simulated signal is processed using wavelet decomposition,and the effect of wavelet decomposition on RBM is evaluated.The phase signal and the processing results after wavelet decomposition are depicted in Figure 5.After performing wavelet decompo-
<header>Electronics 2024,13,1471 9of 20</header>


Electronics 2024,13,1471


9of 20


sition on the phase signal,the FFT spectrum is calculated.The frequency corresponding to the peak with the highest intensity in the spectrum is considered as the heart rate.observed that the heart rate signal cannot be accurately identified when the magnitude of the RBM signal exceeds three times that of the respiratory and heartbeat signals.




Figure 5.Phase and the processing result.(a,b)The simulated time-domain signals with different
magnitudes of RBM.(c,d)The results of phase signal being subjected to wavelet decomposition and FFT.
Figure 5.Phase and the processing result.(a,b)The simulated time-domain signals with different magnitudes of RBM.(c,d)The results of phase signal being subjected to wavelet decomposition and FFT.


The impact of RBM on the EWT analysis method varies with different magnitudes.Figure 5a illustrates the changes in motion on the chest surface when the amplitude of the RBM is equal to the amplitude of the simulated respiratory and heartbeat signals.The processing results are shown in Figure 5c,in which the heart rate corresponds to the peak with the highest intensity in the frequency spectrum.Figure 5b represents changes in motion on the chest surface when the amplitude of RBM is four times that of the simulated respiratory and heartbeat signals.The processing results are depicted in Figure 5d,in which the heart rate peak is overshadowed by interference from other components,leading to inaccurate estimations.Through multiple experimental comparisons,it has been observed that the heart rate signal cannot be accurately identified when the magnitude of the RBM signal exceeds three times that of the respiratory and heartbeat signals.


Identifying and attenuating RBM through the CWT and subsequent wavelet decomposition can be somewhat effective.However,using a fixed number of decomposition levels still fails to resolve RBM issues in more complex scenarios.EWT presents an adaptive wavelet construction method.It decomposes the signal into different modes by designing appropriate wavelet filters,allowing for finer-grained analysis [40].The EWT begins by dividing the signal spectrum and decomposing the input signal into multiple subband signals through the use of various filters.For a given signal s(t),FFT analysis is performed to normalize its frequencies and map them to the range $[0\sim2\pi]$.According to the Shannon criterion,the discussion focuses only on the signal within the support interval [0∼π].The support interval is divided into K segments based on the number of components constituting the signal.


$$\Lambda_{k}=\big[\omega_{k-1},\omega_{k}\big],k=1,2,\cdots,K$$


where ωk is the boundary of each segment,ω0=0,and $\omega_{K}=\pi$.





According to the number of local maxima $M$and parameter K in the spectrum of the signal $s\left(t\right)$,the top min(M,K)extreme points are selected for boundary segmentation.The boundary frequencies are calculated based on the angular frequencies of these extreme
<header>Electronics 2024,13,1471 10of 20</header>


Electronics 2024,13,1471


10of 20


points.The empirical wavelet function and empirical scale function are represented by Equation (15)and Equation (16),respectively.


ˆψk(ω)=
 
      
      
1,(1+γ)ωk ≤|ω|≤(1−γ)ωk+1
cos
�π
2
β
�1
2γωk+1
(|ω|−(1−γ)ωk+1)
��
,(1−γ)ωk+1≤|ω|≤(1+γ)ωk+1
sin
�π
2
β
�1
2γωk
(|ω|−(1−γ)ωk )
��
,(1−γ)ωk ≤|ω|≤(1+γ)ωk
0,otherwise
$$\hat{\phi}_{k}(\omega)=\begin{cases}{1}&{,\lvert\omega\lvert\leq(1-\gamma)\omega_{k}}\\ {\operatorname{c o s}\Bigl[\frac{\pi}{2}\beta\Bigl(\frac{1}{2\gamma\omega_{k}}(\lvert\omega\rvert-(1-\gamma)\omega_{n})\Bigr)\Bigr]}&{,(1-\gamma)\omega_{k}\leq\lvert\omega\rvert\leq(1+\gamma)\omega_{k}}\\ {0}&{,\ h e w i i s}}\\ \{}&{,o t h e r w i s e}\\ \end{cases}$$


$$\hat{\psi}_{k}(\omega)=\begin{cases}{1}&{,(1+\gamma)\omega_{k}\leq|\omega|\leq(1-\gamma)\omega_{k+1}}\\ {\operatorname{c o s}\Big[\frac{\pi}{2}\hat{p\}\Big(\frac{1}{2\gamma\omega_{k+1}}\big(|\omega|-(1-\gamma)\omega_{k+1}\big)\Big)\Big]}&{,(1-\gamma)\omega_{k+1}\leq|\omega|\leq(1+\gamma)\omega_{k+1}}\\ {\operatorname{s i n}\Big[\frac{\pi}{2}\hat{p}\Big(\frac{1}{2\gamma\omega_{k}}\big(|\omega|-(1-\gamma)\omega_{k}\big)\Big)\Big]}&{,(1-\gamma)\omega_{k}\leq|\omega|\leq(1+\gamma)\omega_{k}}\\ {0}&{,t o h h r w w s e}\\ \end{cases}$$








According to [28],the simulated signal is processed using EWT,and the impact of
EWT on RBM is evaluated.After removing the influence of static interference in the signal,the signal is subjected to FFT processing.The strategy of local maxima and minima is employed to determine the number of segments for the support interval,thereby identifying the frequency boundaries.Based on the obtained frequency boundaries,empirical wavelets are constructed to decompose the simulated signal.The decomposed signals are then subjected to FFT transformation to determine the heart rate.
VIEW 11of 21


In the analysis of the impact of the RBM on respiratory and heartbeat signals em-
ploying the EWT method,the RBM amplitude increases from zero.The phase signal and processing results are illustrated in Figure 6.After performing EWT decomposition on the signal,the segment containing the heart rate undergoes the FFT operation.The frequency corresponding to the peak with the highest intensity in the spectrum represents the heart rate.
respiratory and heartbeat signals.The processing results are depicted in Figure 6d,in which the heart rate peak is overshadowed by interference from other components,leading to inaccurate estimations.Through multiple experimental comparisons,it has been observed that when the magnitude of the RBM signal exceeds twice the magnitude of the respiratory and heartbeat signal,the heart rate signal cannot be accurately identified.




Figure 6.Phase and the processing result.(a,b)The simulated time-domain signals with different magnitudes of the RBM.(c,d)The results of the phase signal being subjected to the EWT and FFT.Figure 6.Phase and the processing result.(a,b)The simulated time-domain signals with different magnitudes of the RBM.(c,d)The results of the phase signal being subjected to the EWT and FFT.


Based on the analysis above,it is evident that decomposing and denoising the entire signal is susceptible to strong amount of interference from noise.Additionally,using spectral analysis to obtain the heart rate results in the loss of temporal information provided by the CWT,thereby decreasing its correlation with the variations in heartbeats.Recognizing the characteristics of heartbeat variations and considering the time information The impact of RBM on the EWT analysis method varies with different magnitudes.Figure 6a illustrates the changes in motion on the chest surface when the amplitude of the RBM is equal to the amplitude of the simulated respiratory and heartbeat signals.The processing results are shown in Figure 6c,in which the heart rate corresponds to the peak with the highest intensity in the frequency spectrum.Figure 6b represents changes in
<header>Electronics 2024,13,1471 11of 20</header>


Electronics 2024,13,1471


11of 20


motion on the chest surface when the amplitude of the RBM is three times the simulated respiratory and heartbeat signals.The processing results are depicted in Figure 6d,in which the heart rate peak is overshadowed by interference from other components,leading to inaccurate estimations.Through multiple experimental comparisons,it has been observed that when the magnitude of the RBM signal exceeds twice the magnitude of the respiratory and heartbeat signal,the heart rate signal cannot be accurately


Based on the analysis above,it is evident that decomposing and denoising the entire signal is susceptible to strong amount of interference from noise.Additionally,using spectral analysis to obtain the heart rate results in the loss of temporal information provided by the CWT,thereby decreasing its correlation with the variations in heartbeats.Recognizing the characteristics of heartbeat variations and considering the time information within the CWT,this article proposes a novel method based on previous


# 2.3.Adaptive Motion Artifact Filtering


In terms of micro-motion signals,respiration and heartbeat frequencies are continuously changing over time,and RBM frequency is non-continuously changing over time.Compared to single-spectrum analysis methods,time–frequency analysis methods utilize joint time–frequency distribution to describe the transient characteristics of time series signals and estimate the instantaneous frequency to capture the trends of frequency changes for different signal components over time.The instantaneous frequencies of heartbeat and RBM signals differ at different moments.The energy of the heartbeat signal remains relatively constant,while the energy of RBM randomly fluctuates with the magnitude of motion.Therefore,during moments of high-energy RBM,the components of heartbeat frequency can be overshadowed.The objective of this research is to separate the frequency components of the heartbeat signal from other sources,such as respiratory motion,RBM,and noise.Therefore,we propose the AMF


When analyzing the signal using CWT,multiple components may be present in the resulting spectrum.To address interference from other components,a detection process is employed to identify spectral peaks within each time–frequency slice.These peaks are then compared with the peaks from adjacent time slices.Subsequently,the components are divided,and the constituent components within the signal are determined.Based on the characteristics of heart rate frequency variations,the component corresponding to the heartbeat signal is


In the obtained spectrum peaks,it is not possible to solely differentiate clutter signal components from heartbeat signal components based on the intensity of the peaks due to the influence of clutter components'strength.To address this issue,a method is proposed to distinguish different signal components based on the frequency variation relationship among the components.Consequently,a signal component segmentation approach utilizing image processing techniques is employed [41].The specific algorithmic procedure is outlined as follows:


(a)Determine the position of each spectral peak at every time point;
(b)The spectral peaks within the time at t are selected as the starting points for component fitting;
(c)Along the temporal axis,the frequency of the spectral peak corresponding to tk and the differences in spectral peak frequencies between [tk+1,tk+2,tk+3]are calculated,respectively.The spectral peak with the smallest difference is se-lected for fitting;
(d)The process described in (c)is repeated until all time points have been traversed;
(e)The peak-to-peak value of the fitted curve is calculated,and the signal component with the smallest peak-to-peak value is selected as the heart rate
<header>Electronics 2024,13,1471 12of 20</header>


Electronics 2024,13,1471


12of 20


The impact of different intensities of the RBM on the algorithm performance varies.
Figure 7a illustrates the motion variation on the chest surface when the simulated respiratory and heartbeat signals overlap with the RBM signal with an amplitude of 1.The processing result is shown in Figure $\ {sf nabla c},$in which the heart rate continuously changes over time and can be accurately extracted.In Figure 7b,the chest surface motion is depicted when the simulated respiratory and heartbeat signals overlap with the RBM signal with an amplitude of 6.The processing result is shown in Figure 7d,in which the spectral peak corresponding to the heartbeat signal is completely submerged after 6s,making it impossible to extract the peak information and obtain accurate estimations.Through multiple experimental comparisons,it was observed that when the amplitude of the RBM signal exceeds five times the amplitude of the respiratory and heartbeat signals,the heart rate signal cannot be accurately identified.The impact of different intensities of the RBM on the algorithm performance varies.
Figure 7a illustrates the motion variation on the chest surface when the simulated respiratory and heartbeat signals overlap with the RBM signal with an amplitude of 1.The processing result is shown in Figure 7which the heart rate continuously changes over time and can be accurately extracted.In Figure 7b,the chest surface motion is depicted when the simulated respiratory and heartbeat signals overlap with the RBM signal with an amplitude of 6.The processing result is shown in Figure 7d,in which the spectral peak corresponding to the heartbeat signal is completely submerged after 6s,making it impossible to extract the peak information and obtain accurate estimations.Through multiple experimental comparisons,it was observed that when the amplitude of the RBM signal exceeds five times the amplitude of the respiratory and heartbeat signals,the heart rate signal cannot be accurately identified.




Figure 7.Phase and the processing result.(a,b)The simulated time-domain signals with different
magnitudes of RBM.(c,d)The results of the phase signal being subjected to the AMF.
Figure 7.Phase and the processing result.(a,b)The simulated time-domain signals with different magnitudes of RBM.(c,d)The results of the phase signal being subjected to the AMF.


The impact of low-amplitude RBM on the algorithm is relatively small.However,as the RBM amplitude increases,the relative strength of the heartbeat signal decreases compared to that of the RBM,leading to the submergence of the heartbeat signal and inaccurate detection.Figure 8a illustrates the computational results of different algorithms when the amplitude of the RBM is equal to the amplitude of the simulated respiratory and heartbeat signals.The simulation results indicate that the influence of lower RBM amplitudes on the class of algorithms based on the CWT can be mostly ignored.Figure 8b presents the computational results of different algorithms when the RBM amplitude is five times the simulated signal amplitude.The simulation results indicate that a key issue affecting the accurate detection of heart rate by the algorithms is the submergence of the heartbeat signal due to the increased RBM amplitude.The proposed AMF algorithm utilizes the temporal information of each component,reducing the impact of high-amplitude RBM on the heartbeat signal.However,other methods struggle to effectively mitigate the impact of high-amplitude RBM,leading to erroneous detection outcomes.
<header>Electronics 2024,13,1471 13of 20</header>


Electronics 2024,13,1471


13of 20




Figure 8.The simulation comparison results between the AMF and other methods are presented.
(a)The computational results of different algorithms under the RBM with an amplitude of one are presented.(b)The computational results of different algorithms under the RBM with an amplitude of five are presented.
Figure 8.The simulation comparison results between the AMF and other methods are presented.(a)The computational results of different algorithms under the RBM with an amplitude of one are presented.(b)The computational results of different algorithms under the RBM with an amplitude of five are presented.


# 3.Results 3.Results


The algorithm's performance was evaluated through experimental assessments us-
ing an MIMO mmWave radar.The results were compared with those obtained from a contact-based sensor electrocardiogram (ECG)monitor and other recent techniques to verify the efficacy of the proposed approach.The algorithm's performance was evaluated through experimental assessments using
an MIMO mmWave radar.The results were compared with those obtained from a contactbased sensor electrocardiogram (ECG)monitor and other recent techniques to verify the efficacy of the proposed approach.


The experiments were conducted in a neonatal intensive care unit,as depicted in Fig-
ure 9,which illustrates the experimental setup including the radar sensors and electrocardiogram (ECG)monitor.The participants consisted of three infants with specific health conditions,as outlined in Table 1.One participant was a mid-term premature infant,who may have various risks due to the incomplete development of his or her organ systems compared to those of full-term infants.These risks include respiratory complications such as apnea and respiratory distress syndrome,resulting from an underdeveloped respiratory system.Additionally,the incomplete development of the circulatory system may lead to complications such as persistent pulmonary hypertension and heart failure.Another participant was a term infant diagnosed with neonatal wet lung,a condition characterized by respiratory difficulties caused by the inadequate clearance of fluid from the lungs.Symptoms may include grunting,froth,and inspiratory indrawing.The last participant was also a term infant diagnosed with meconium aspiration and mild asphyxia.Asphyxia-induced hypoxia may lead to oxygen deprivation in various systems,resulting in complications such as feeding intolerance and necrotizing enterocolitis in the digestive The experiments were conducted in a neonatal intensive care unit,as depicted in
Figure 9,which illustrates the experimental setup including the radar sensors and electrocardiogram (ECG)monitor.The participants consisted of three infants with specific health conditions,as outlined in Table 1.One participant was a mid-term premature infant,who may have various risks due to the incomplete development of his or her organ systems compared to those of full-term infants.These risks include respiratory complications such as apnea and respiratory distress syndrome,resulting from an underdeveloped respiratory system.Additionally,the incomplete development of the circulatory system may lead to complications such as persistent pulmonary hypertension and heart failure.Another participant was a term infant diagnosed with neonatal wet lung,a condition characterized by respiratory difficulties caused by the inadequate clearance of fluid from the lungs.Symptoms may include grunting,froth,and inspiratory indrawing.The last participant was also a term infant diagnosed with meconium aspiration and mild asphyxia.Asphyxia-induced hypoxia may lead to oxygen deprivation in various systems,resulting in complications such as feeding intolerance and necrotizing enterocolitis in the digestive system,as well as hypoxic-ischemic encephalopathy in the nervous system.


Table 1.The specific characteristics of the study participants.


|Study Participants|Gestational Age|Weight|Age|Symptoms|
|:---|:---|:---|:---|:---|
|Baby1|39 weeksand5days|3180g|4days|Newborn wet lung|
|Baby2|33 weeks and5days|1840g|14 days|Premature birth|
|Baby3|39 weeksand2 days|3710g|4days|Amnioticfluid inhalation,mild suffocation|



The MIMO mmWave radar used for evaluation was the vTrig mmWave sensor evaluation kit produced by Vayyar.The radar system was equipped with 20transmitting (Tx)and 20receiving (Rx)onboard antennas,enabling the transmission of SFCW waveforms in the frequency range of 62–69GHz.The radio signal power emitted by the radar was below −10dBm,significantly lower than the radio power of mobile phones or WiFi devices.The structure of the radar system is illustrated in Figure 10a.The MIMO architecture allowed for an effective array of 400virtual elements,as shown in Figure 10b.This radar system had a large effective aperture,resulting $\operatorname{i n}a\operatorname{h i g h}$resolution in both the azimuth
<header>Electronics 2024,13,1471 14of 20</header>


Electronics 2024,13,1471


14of 20


and elevation directions.Table 2presents the important parameters related to the radar
signal.For subsequent experiments,a bandwidth of 1.6GHz was set to balance the data rate and image resolution.The frame rate was set at 30Hz.
Baby139weeks and 5days 3180g 4days Newborn wet lung
Baby233weeks and 5days 1840g 14days Premature birth
Baby339weeks and 2days 3710g 4days
Amniotic fluid inhala-
tion,mild suffocation




Figure 9.The experimental environment and equipment.Figure 9.The experimental environment and


The MIMO mmWav Table 2.Radar


|Parameters|Value|
|:---|:---|
|Frequency Band|62-69GHz|
|ADC Samples|151|
|Stop-StartMin Step|150MHz|
|EIRP(EffectiveIsotropicRadiatedPower|-5dBm|
|MaxRangeResolution|2.14 cm|
|MaxAngularResolution|6.7°|





Figure 10.Radar internal structure.(a)Radar system structure.(b)Radar virtual antenna array Figure 10.Radar internal structure.(a)Radar system structure.(b)Radar virtual antenna array


element.The accuracy of non-contact vital sign detection results needs to be compared with The accuracy of non-contact vital sign detection results needs to be compared with that of the gold standard,contact-based heart rate measurements.Accurate heart rate readings
<header>Electronics 2024, 13, 1471 15 of 20</header>


Electronics 2024, 13, 1471


15 of 20


were obtained using the ePM 10 Neo patient monitor manufactured by Mindray. The laptop
computer was utilized for radar data acquisition and processing. The radar measurements
were synchronized with the reference values provided by the patient monitor through the
computer and the electrocardiogram (ECG) monitor's internal clock.


After recording the data, the multi-channel data underwent beamforming processing,
aligning the beams towards the subject's chest. The resulting echoes from the beamforming
process were extracted, and after removing the static clutter, the phase information on the
surface of the subject's chest was obtained, as depicted in Figure 11. Figure 11 consists of
nine phase results, and each row represents the phase information of a different newborn.
Rows 1 to 3 correspond to baby 1, baby 2, and baby 3, respectively, while each column
represents a specific state. The first column represents the phase variation in a stationary
state, whereas the second and third columns represent the phase variation during the
occurrence of RBM.
VIEW 16 of 21




$^2$


Figure 11. The phase variations on the surface of the chest under different states were observed
across different subjects. Rows 1 to 3 correspond to babies 1 to 3. Column 1 corresponds to the stationary state, and columns 2 and 3 correspond to the RBM state.
Figure 11. The phase variations on the surface of the chest under different states were observed across
different subjects. Rows 1 to 3 correspond to babies 1 to 3. Column 1 corresponds to the stationary
state, and columns 2 and 3 correspond to the RBM state.


The first-order differencing technique was applied to the phase on the chest surface to
accentuate the heartbeat details. Then a signal analysis using the CWT was performed, as
illustrated in Figure 12. During periods of relative stillness, the intensity of the heartbeat
frequency component was relatively high. However, when the subjects experienced RBM,
the intensity of the heartbeat frequency component varied at different time points and was
sometimes overshadowed by other components.


The AMF method was applied to further process the results of the wavelet transform,
allowing for the separation of the cardiac component and the clutter component based on
the relationship between the spectral peaks at adjacent time points. Figure 13 illustrates
the extraction results of the CWT spectral peaks shown in Figure 12, as well as the final
obtained cardiac component. From Figure 13, it can be observed that the acquisition of the
cardiac component is not influenced by its intensity. Even when the intensity of the cardiac
component is lower than that of other components, as long as the cardiac component is
<header>Electronics 2024, 13, 1471 16 of 20</header>


Electronics 2024, 13, 1471


16 of 20


not completely overshadowed, it can be obtained through the continuous characteristics of
the heartbeat.
across different subjects. Rows 1 to 3 correspond to babies 1 to 3. Column 1 corresponds to the stationary state, and columns 2 and 3 correspond to the RBM state.




Figure 12. Signal analysis using the CWT was applied to examine the variations across different
subjects and states. Rows 1 to 3 correspond to babies 1 to 3. Column 1 corresponds to the stationary
state, and columns 2 and 3 correspond to the RBM state.
Figure 12. Signal analysis using the CWT was applied to examine the variations across different
subjects and states. Rows 1 to 3 correspond to babies 1 to 3. Column 1 corresponds to the stationary
state, and columns 2 and 3 correspond to the RBM state.
VIEW 17 o




Figure 13. The processing results after applying the AMF method for different subjects under v
ous states. Rows 1 to 3 correspond to babies 1 to 3. Column 1 corresponds to the stationary s
and columns 2 and 3 correspond to the RBM state.
Figure 13. The processing results after applying the AMF method for different subjects under various
states. Rows 1 to 3 correspond to babies 1 to 3. Column 1 corresponds to the stationary state, and
columns 2 and 3 correspond to the RBM state.
<header>Electronics 2024,13,1471 17of 20</header>


Electronics 2024,13,1471


17of 20


The final results demonstrate that the proposed method successfully extracts the
cardiac component,which closely aligns with the heartbeat measurements obtained through ECG,as depicted in Figure 14.In comparison to other methods,the proposed approach fully utilizes the temporal and frequency characteristics of the signal.By decomposing the signal,it effectively captures the frequency components at different time points and exhibits an advantage in removing clutter components.Furthermore,it enables the assessment of temporal variations in heart rate.The final results demonstrate that the proposed method successfully extracts the car-
diac component,which closely aligns with the heartbeat measurements obtained through ECG,as depicted in Figure 14.In comparison to other methods,the proposed approach fully utilizes the temporal and frequency characteristics of the signal.By decomposing the signal,it effectively captures the frequency components at different time points and exhibits an advantage in removing clutter components.Furthermore,it enables the assessment of temporal variations in heart rate.




$\underline{{\underline{{\phantom{\ }}}}}_underline{{{\mathrmmathrm{font~:}}}}^{\mathrm{A M F}}\underline{{\underline{{\phantom{\ }}}}}_{\mathrm{E C G}}^{\mathrm{F W T}}$


Figure 14.The comparison results between the AMF and other methods.Rows 1to 3correspond to
babies 1to 3.Column 1corresponds to the stationary state,and columns 2and 3correspond to the RBM state.
Figure 14.The comparison results between the AMF and other methods.Rows 1to 3correspond to babies 1to 3.Column 1corresponds to the stationary state,and columns 2and 3correspond to the RBM state.


After acquiring the cardiac signal,the accuracy (ACC),average absolute error (MAE),and root mean square error (RMSE)of the measurement results were calculated [42,43].The formulas for these calculations are shown as Equations (16)–(18).


$$A C C=1-\frac{\left|H R_{e s t}-H R_{r e f}\right|}{H R_{r e f}}$$


$$M A E=\frac{1}{N}{\sum}\Big|H R_{e s t}-H R_{r e f}\Big|$$


$$R M S E=\sqrt{\frac{1}{N}{\sum\left(H R_{e s t}-H R_{r e f}\right)}.^{2}}$$











In order to further quantify the performance of the proposed adaptive RBM removal method,multiple experiments were conducted using different subjects and various motion states.The first set of experiments involved subjects in a stationary state,while the second set included subjects experiencing RBM,such as newborn hiccups,tremors,seizures,and limb movements.The accuracy of the HR measurements for the multiple sets of data in the stationary state was 97%,while in the motion state,they had a high accuracy of 96%.Furthermore,a detailed analysis of the results was conducted.


The performance of the AMF method across different individuals is elaborated in Table 3.The results indicate minimal variations in HR accuracy across the different states
<header>Electronics 2024,13,1471 18of 20</header>


Electronics 2024,13,1471


18of 20


among the individuals.However,significant differences were observed in the MAE and RMSE among the different individuals,with baby 2exhibiting particularly exceptional results.A further analysis of the individual's condition revealed that baby 2was a premature infant with a low level of muscle tone and reduced physiological movement compared to a typical newborn,resulting in a lower activity frequency.Hence,relatively better results were obtained for this


Table 3.The performance evaluation results of the AMF


<table><tr><td rowspan="2">Study Participants</td><td colspan="2">ACC(%)</td><td colspan="2">MAE (bpm)</td><td colspan="2">RMSE (bpm)</td></tr><tr><td>Static</td><td>Movement</td><td>Static</td><td>Movement</td><td>Static</td><td>Movement</td></tr><tr><td>Baby1</td><td>96.4</td><td>96.3</td><td>4.6</td><td>4.7</td><td>5.4</td><td>5.8</td></tr><tr><td>Baby2</td><td>99.4</td><td>96.4</td><td>0.7</td><td>3.1</td><td>1.0</td><td>3.6</td></tr><tr><td>Baby3</td><td>97.6</td><td>96.2</td><td>3.0</td><td>4.6</td><td>3.6</td><td>5.7</td></tr></table>


# 4.Discussion and Conclusions


This paper's method was also compared with other recent wavelet-based methods,as shown in Table 4.In conclusion,the processing workflow proposed in this paper demonstrates a superior performance in terms of its HR accuracy (ACC),average absolute error (MAE),and root mean square error (RMSE)compared to those of the other methods,particularly in the presence of RBM.This can be attributed to two main factors.For one,during the preprocessing stage,the MIMO mmWave radar utilizes digital beamforming (DBF)to physically focus the beam,suppressing interference from surrounding objects,individuals,and limbs outside the thoracic cavity.Additionally,the AMF method successfully mitigates the impact of high-intensity clutter on the cardiac signal components by addressing the inherent variations in the heartbeat signal.Although we have validated the performance of the proposed method in the current scenario,further explorations of signals from the chest surface are necessary to optimize its performance in more complex cardiopulmonary resuscitation


Table 4.The performance evaluation results of different


<table><tr><td rowspan="2">Method</td><td colspan="2">ACC(%)</td><td colspan="2">MAE (bpm)</td><td colspan="2">RMSE (bpm)</td></tr><tr><td>Static</td><td>Movement</td><td>Static</td><td>Movement</td><td>Static</td><td>Movement</td></tr><tr><td>Method1[31]</td><td>94.1</td><td>89.8</td><td>7.7</td><td>13.4</td><td>7.7</td><td>13.8</td></tr><tr><td>Method2 [28]</td><td>98.1</td><td>88.1</td><td>2.4</td><td>15.9</td><td>2.5</td><td>16.2</td></tr><tr><td>AMF</td><td>97.9</td><td>96.6</td><td>2.8</td><td>4.6</td><td>3.3</td><td>5.1</td></tr></table>


In the current experiments,the relative angle between the newborn and the radar remains relatively fixed.However,in more complex neonatal resuscitation scenarios,the angle between the newborn's chest and the radar may vary.Therefore,in future studies,it is necessary to explore more optimal beamforming techniques to focus the radar beam on the chest and suppress the surrounding interference.In the presence of more severe RBM,there may be instances in which the cardiac signal component is completely overwhelmed.Hence,further explorations of signal decomposition methods are necessary to mitigate the impact of RBM on the


impact of RBM on the heartbeat.The accuracy of the AMF method for detecting neonatal respiratory rate has been validated in this article;however,it has been found that some steps still cannot be adaptively adjusted.For instance,after the neonate's position changes,it has been observed that the beamforming is unable to automatically identify the location of the neonate's chest.In future research,it is planned to determine the chest's location by mining the differences between the chest and other signal features in the space over a period of time.This information will be utilized to guide the radar in performing adaptive beamforming at the chest's location,which is expected to further improve the accuracy of the
<header>Electronics 2024,13,1471 19of 20</header>


Electronics 2024,13,1471


# References


19of 20


Furthermore,preparations are being made to integrate the AMF system with other medical monitoring equipment,with the aim of providing a more comprehensive solution for the detection of neonatal vital


Author Contributions:Conceptualization,S.Y.and X.L.;methodology,S.Y.and Y.L.;software,S.Y.;validation,S.Y.,N.J.,J.C.and Z.Z.;formal analysis,Y.L.and S.Y.;investigation,S.Y.,X.L.,Z.Z.and J.C.;resources,X.L.and X.D.;data curation,X.L.and X.D.;writing—original draft preparation,S.Y.;writing—review and editing,S.Y.,Y.L.and X.D.;visualization,S.Y.;supervision,Y.L.;project administration,X.D.;funding acquisition,Y.L.All authors have read and agreed to the published version of the


Funding:This research was funded by the National Natural Science Foundation of China (Grant


Institutional Review Board Statement:The study was conducted according to the guidelines of the Declaration of Helsinki and approved by the Ethics Committee of Peking University Third Hospital Medical Science Research Ethics Committee (Medical Ethics Approval


Data Availability Statement:The data can be shared up on reque


Acknowledgments:The authors would like to thank the reviewers and editors for their help in improving our


Conflicts of Interest:The authors declare no conflicts of


1.Perin,J.;Mulick,A.;Yeung,D.;Villavicencio,F.;Lopez,G.;Strong,K.L.;Prieto-Merino,D.;Cousens,S.;Black,R.E.;Liu,L.
Global,regional,and national causes of under-5mortality in 2000–19:An updated systematic analysis with implications for the Sustainable Development Goals.Lancet Child Adolesc.Health 2022,6,106–115.[CrossRef][PubMed]
2.Wiswell,T.E.Neonatal resuscitation.Respir.Care 2003,48,288–294;discussion 294–295.[PubMed]
3.Garvey,A.A.;Dempsey,E.M.Simulation in Neonatal Resuscitation.Front.Pediatr.2020,8,59.[CrossRef][PubMed]
4.Fang,J.L.;Umoren,R.A.Telesimulation for Neonatal Resuscitation Training.Semin.Perinatol.2023,47,151827.[CrossRef][PubMed]
5.Flower,A.A.;Moorman,J.R.;Lake,D.E.;Delos,J.B.Periodic heart rate decelerations in premature infants.Exp.Biol.Med.2010,235,531–538.[CrossRef][PubMed]
6.Johnson,P.A.;Schmölzer,G.M.Heart rate assessment during neonatal resuscitation.Healthcare 2020,8,43.[CrossRef]
7.Topfer,F.;Oberhammer,J.Millimeter-wave tissue diagnosis:The most promising fields for medical applications.IEEE Microw.Mag.2015,16,97–113.[CrossRef]
8.Anton,O.;Fernandez,R.;Rendon-Morales,E.;Aviles-Espinosa,R.;Jordan,H.;Rabe,H.Heart rate monitoring in newborn babies:A systematic review.Neonatology 2019,116,199–210.[CrossRef][PubMed]
9.Verkruysse,W.;Svaasand,L.O.;Nelson,J.S.Remote plethysmographic imaging using ambient light.Opt.Express 2008,16,21434–21445.[CrossRef]
10.Kumar,M.;Veeraraghavan,A.;Sabharwal,A.DistancePPG:Robust non-contact vital signs monitoring using a camera.Biomed.Opt.Express 2015,6,1565–1588.[CrossRef]
11.Ravichandran,R.;Saba,E.;Chen,K.-Y.;Goel,M.;Gupta,S.;Patel,S.N.WiBreathe:Estimating respiration rate using wireless signals in natural settings in the home.In Proceedings of the 2015IEEE International Conference on Pervasive Computing and Communications (PerCom),St.Louis,MO,USA,23–27March 2015;pp.131–139.
12.Patwari,N.;Brewer,L.;Tate,Q.;Kaltiokallio,O.;Bocca,M.Breathfinding:A wireless network that monitors and locates breathing in a home.IEEE J.Sel.Top.Signal Process.2013,8,30–42.[CrossRef]
13.Liu,X.;Cao,J.;Tang,S.;Wen,J.Wi-sleep:Contactless sleep monitoring via wifi signals.In Proceedings of the 2014IEEE Real-Time Systems Symposium,Rome,Italy,2–5December 2014;pp.346–355.
14.Lin,J.C.Noninvasive microwave measurement of respiration.Proc.IEEE 1975,63,1530.[CrossRef]
15.Li,C.;Ling,J.;Li,J.;Lin,J.Accurate Doppler radar noncontact vital sign detection using the RELAX algorithm.IEEE Trans.Instrum.Meas.2009,59,687–695.
16.Xiong,Y.;Chen,S.;Dong,X.;Peng,Z.;Zhang,W.Accurate measurement in Doppler radar vital sign detection based on parameterized demodulation.IEEE Trans.Microw.Theory Tech.2017,65,4483–4492.[CrossRef]
17.Saluja,J.;Casanova,J.;Lin,J.A supervised machine learning algorithm for heart-rate detection using Doppler motion-sensing radar.IEEE J.Electromagn.RF Microw.Med.Biol.2019,4,45–51.[CrossRef]
18.Feng,C.;Jiang,X.;Jeong,M.-G.;Hong,H.;Fu,C.-H.;Yang,X.;Wang,E.;Zhu,X.;Liu,X.Multitarget vital signs measurement with chest motion imaging based on MIMO radar.IEEE Trans.Microw.Theory Tech.2021,69,4735–4747.[CrossRef]
<header>Electronics 2024,13,1471 20of 20</header>


Electronics 2024,13,1471


20of 20


19.Cardillo,E.;Caddemi,A.A review on biomedical MIMO radars for vital sign detection and human localization.Electronics 2020,
9,1497.[CrossRef]
20.Upadhyay,B.R.;Baral,A.B.;Torlak,M.Vital sign detection via angular and range measurements with mmWave MIMO radars:Algorithms and trials.IEEE Access 2022,10,106017–106032.[CrossRef]
21.Kim,J.D.;Lee,W.H.;Lee,Y.;Lee,H.J.;Cha,T.;Kim,S.H.;Song,K.-M.;Lim,Y.-H.;Cho,S.H.;Cho,S.H.Non-contact respiration monitoring using impulse radio ultrawideband radar in neonates.R.Soc.Open Sci.2019,6,190149.[CrossRef]
22.Lee,W.H.;Lee,Y.;Na,J.Y.;Kim,S.H.;Lee,H.J.;Lim,Y.-H.;Cho,S.H.;Cho,S.H.;Park,H.-K.Feasibility of non-contact cardiorespiratory monitoring using impulse-radio ultra-wideband radar in the neonatal intensive care unit.PLoS ONE 2020,15,e0243939.[CrossRef]
23.Park,J.-Y.;Lee,Y.;Heo,R.;Park,H.-K.;Cho,S.-H.;Cho,S.H.;Lim,Y.-H.Preclinical evaluation of noncontact vital signs monitoring using real-time IR-UWB radar and factors affecting its accuracy.Sci.Rep.2021,11,23602.[CrossRef][PubMed]
24.Gu,C.;Wang,G.;Inoue,T.;Li,C.Doppler radar vital sign detection with random body movement cancellation based on adaptive phase compensation.In Proceedings of the 2013IEEE MTT-S International Microwave Symposium Digest (MTT),Seattle,WC,USA,2–7June 2013;pp.1–3.
25.Li,C.;Lin,J.Random Body Movement Cancellation in Doppler Radar Vital Sign Detection.IEEE Trans.Microw.Theory Tech.2008,56,3143–3152.[CrossRef]
26.Wang,F.K.;Horng,T.S.;Peng,K.C.;Jau,J.K.;Li,J.Y.;Chen,C.C.Single-Antenna Doppler Radars Using Self and Mutual Injection Locking for Vital Sign Detection With Random Body Movement Cancellation.IEEE Trans.Microw.Theory Tech.2011,59,3577–3587.[CrossRef]
27.Yu,X.;Li,C.;Lin,J.Two-dimensional noncontact vital sign detection using Doppler radar array approach.In Proceedings of the 2011IEEE MTT-S International Microwave Symposium,Baltimore,MD,USA,5–10June 2011;pp.1–4.
28.Zhang,X.;Yang,X.;Ding,Y.;Wang,Y.;Zhou,J.;Zhang,L.Contactless simultaneous breathing and heart rate detections in physical activity using ir-uwb radars.Sensors 2021,21,5503.[CrossRef][PubMed]
29.Lv,Q.;Chen,L.;An,K.;Wang,J.;Li,H.;Ye,D.;Huangfu,J.;Li,C.;Ran,L.Doppler Vital Signs Detection in the Presence of Large-Scale Random Body Movements.IEEE Trans.Microw.Theory Tech.2018,66,4261–4270.[CrossRef]
30.Tariq,A.;Shiraz,H.Doppler radar vital signs monitoring using wavelet transform.In Proceedings of the 2010Loughborough Antennas &Propagation Conference,Loughborough,UK,8–9November 2010;pp.293–296.
31.Mercuri,M.;Lorato,I.R.;Liu,Y.-H.;Wieringa,F.;Hoof,C.V.;Torfs,T.Vital-sign monitoring and spatial tracking of multiple people using a contactless radar-based sensor.Nat.Electron.2019,2,252–262.[CrossRef]
32.He,M.;Nian,Y.;Xu,L.;Qiao,L.;Wang,W.Adaptive separation of respiratory and heartbeat signals among multiple people based on empirical wavelet transform using UWB radar.Sensors 2020,20,4913.[CrossRef][PubMed]
33.Ren,L.;Kong,L.;Foroughian,F.;Wang,H.;Theilmann,P.;Fathy,A.E.Comparison Study of Noncontact Vital Signs Detection Using a Doppler Stepped-Frequency Continuous-Wave Radar and Camera-Based Imaging Photoplethysmography.IEEE Trans.Microw.Theory Tech.2017,65,3519–3529.[CrossRef]
34.Harter,M.;Mahler,T.;Schipper,T.;Ziroff,A.;Zwick,T.2-D antenna array geometries for MIMO radar imaging by Digital Beamforming.In Proceedings of the 2013European Microwave Conference,Nuremberg,Germany,6–10October 2013;pp.1695–1698.
35.Wang,G.;Muñoz-Ferreras,J.M.;Gu,C.;Li,C.;Gómez-García,R.Application of Linear-Frequency-Modulated Continuous-Wave (LFMCW)Radars for Tracking of Vital Signs.IEEE Trans.Microw.Theory Tech.2014,62,1387–1399.[CrossRef]
36.Zhang,X.-D.Modern Signal Processing;Walter de Gruyter GmbH &Co KG:Berlin,Germany,2022.
37.Rana,M.J.;Alam,M.S.;Islam,M.S.Continuous wavelet transform based analysis of low frequency oscillation in power system.In Proceedings of the 2015International Conference on Advances in Electrical Engineering (ICAEE),Dhaka,Bangladesh,17–19December 2015;pp.320–323.
38.Hu,X.;Jin,T.Short-range vital signs sensing based on EEMD and CWT using IR-UWB radar.Sensors 2016,16,2025.[CrossRef]39.Addison,P.S.;Watson,J.N.;Feng,T.Low-oscillation complex wavelets.J.Sound Vib.2002,254,733–762.[CrossRef]
40.Gilles,J.Empirical wavelet transform.IEEE Trans.Signal Process.2013,61,3999–4010.[CrossRef]
41.Jähne,B.Digital Image Processing;Springer Science &Business Media:Berlin/Heidelberg,Germany,2005.
42.Xiong,Y.;Peng,Z.;Gu,C.;Li,S.;Wang,D.;Zhang,W.Differential Enhancement Method for Robust and Accurate Heart Rate Monitoring via Microwave Vital Sign Sensing.IEEE Trans.Instrum.Meas.2020,69,7108–7118.[CrossRef]
43.Li,Z.;Jin,T.;Dai,Y.;Song,Y.Motion-Robust Contactless Heartbeat Sensing Using 4-D Imaging Radar.IEEE Trans.Instrum.Meas.2023,72,4011110.[CrossRef]


Disclaimer/Publisher's Note:The statements,opinions and data contained in all publications are solely those of the individual author(s)and contributor(s)and not of MDPI and/or the editor(s).MDPI and/or the editor(s)disclaim responsibility for any injury to people or property resulting from any ideas,methods,instructions or products referred to in the
