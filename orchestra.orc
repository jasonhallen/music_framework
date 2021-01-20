<CsoundSynthesizer>
<CsOptions>
-odac
</CsOptions>
<CsInstruments>
sr = 44100
ksmps = 64
0dbfs = 1
nchnls = 2

instr 100 ; STRING PLUCK
    ;p3=p4
    seed 0
    irefl	random 0.001, 0.4
    aEnv	linsegr	0, 0.005, 1, p3-0.105, 1, 0.1, 0		; amplitude envelope
    iPlk	random	0.1, 0.6					; point at which to pluck the string
    iDtn	random    -0.05, 0.05					; random detune
    ;irefl	table	inum, giScal1					; read reflection value from giScal table according to note number
    aSig	wgpluck2  0.58, p4, cpspch(p5), iPlk, irefl	; generate Karplus-Strong plucked string audio
    kcf	expon	cpsoct(rnd(6)+6),p3,50				; filter cutoff frequency envelope
    aSig	clfilt	aSig, kcf, 0, 2					; butterworth lowpass filter
    chnmix aSig*aEnv*1*p6, "mixl"
	chnmix aSig*aEnv*1*p6, "mixr"
endin

instr 101 ; ORGAN
    ;p3=p4
    ifrq = cpspch(p5)
    kenv madsr 0.001,0.1,0.7,0.1
    a1     oscili 8/43,   1      * ifrq
    a2     oscili 8/43,   2      * ifrq
    a3     oscili 8/43,   2.9966 * ifrq
    a4     oscili 8/43,   4      * ifrq
    a5     oscili 3/43,   5.9932 * ifrq
    a6     oscili 2/43,   8      * ifrq
    a7     oscili 1/43,  10.0794 * ifrq
    a8     oscili 1/43,  11.9864 * ifrq
    a9     oscili 4/43,  16      * ifrq
    asig = kenv*p4*0.6*(a1+a2+a3+a4+a5+a6+a7+a8+a9)
    chnmix asig*p6*0.5, "mixl"
    chnmix asig*p6*0.5, "mixr"
endin

instr 102 ; B3 ORGAN
    ;p3=p4
    kfreq cpspch p5
    kc1 = 0.5
    kc2 = 0.5
    kvrate = 6

    kenv madsr 0.001,0.1,0.7,0.1
    kvdpth line 0, p3, 0.1
    asig   fmb3 kenv*p4*2.3, kfreq, kc1, kc2, kvdpth, kvrate
    chnmix asig*p6*0.7, "mixl"
	chnmix asig*p6*0.7, "mixr"
endin

instr 103 ; FLUTE
    ;p3=p4
    kfreq = cpspch(p5)
    kc1 = 5
    kvdepth = .01
    kvrate = 6

    kenv expseg 0.001,0.1,p4,p3-0.2,p4,0.1,0.001
    kc2  line 5, p3, p5
    asig fmpercfl kenv, kfreq, kc1, kc2, kvdepth, kvrate
    chnmix asig, "mixl"
	chnmix asig, "mixr"
endin

instr 104 ; VOICE
    ;p3 = p4
    kfreq cpspch p6
    kvowel = int(random(0,12))	; p4 = vowel (0 - 64)
    ktilt  = 99
    kvibamt = 0.01
    kvibrate = 5

    kenv adsr 0.01,0.1,0.8,0.1
    asig fmvoice p5*kenv, kfreq, kvowel, ktilt, kvibamt, kvibrate
    chnmix asig, "mixl"
	chnmix asig, "mixr"
endin

instr 105 ; RHODES
    seed 0
    ;p3=p4
    kfreq = cpspch(p5)
    kc1 = int(random(1,6))
    kc2 = 0
    kvdepth = 0.4
    kvrate = 3
    ifn1 = -1
    ifn2 = -1
    ifn3 = -1
    ifn4 = 53
    ivfn = -1
    ;kenv expseg 0.00001,0.01,p4,p3-0.11,p4,0.1,0.00001
    kenv linseg 0,0.01,p4,p3-0.11,p4,0.1,0
    asig fmrhode kenv, kfreq, kc1, kc2, kvdepth, kvrate, ifn1, ifn2, ifn3, ifn4, ivfn
    chnmix asig*p6*0.5, "mixl"
	chnmix asig*p6*0.5, "mixr"
endin

instr 106 ; MARIMBA
    ifreq = cpspch(p5)
    ihrd = 0.1
    ipos = 0.561
    imp = 54
    kvibf = 6.0
    kvamp = 0.05
    ivibfn = 2
    idec = 0.6

    asig marimba p4*1, ifreq, ihrd, ipos, imp, kvibf, kvamp, ivibfn, idec, 0.001, 0.001

    chnmix asig*p6*3, "mixl"
    chnmix asig*p6*3, "mixr"
endin

instr 107 ; MOOG
    ;ktrig = (release() == 1 ? 0 : 1)
    ifreq = cpspch(p5)
    iatt1 = 0.01
    idec1 = 0.1
    isus1 = 0.8
    irel1 = 0.1
    kenv1 madsr iatt1,idec1,isus1,irel1 ;ADSR p4,iatt1,idec1,isus1,irel1,ktrig
    iatt2 = 0.1
    idec2 = 0.2
    isus2 = 0.4
    irel2 = 0.05
    kenv2 madsr iatt2,idec2,isus2,irel2 ;ADSR 1,iatt2,idec2,isus2,irel2,ktrig
    a1 vco2 1/3, ifreq
    a2 vco2 1/3, ifreq*1.005
    a3 vco2 1/3, ifreq*.995
    a4 moogladder a1+a2+a3, ifreq*6*(1+kenv2), 0.7
    asig = a4*kenv1*p4*1.8

    chnmix asig*p6, "mixl"
    chnmix asig*p6, "mixr"
endin

opcode VocBand,a,aakk
    as,an,kf,kbw xin
    xout(balance(butterbp(butterbp(as,kf,kbw),kf,kbw),butterbp(butterbp(an,kf,kbw),kf,kbw)))
endop

opcode Vocoder,a,aakkkpp
    as,an,kmin,kmax,kq,ibnd,icnt xin
    if kmax < kmin then
        ktemp = kmin
        kmin = kmax
        kmax = ktemp
    endif
    if kmin == 0 then
        kmin = 1
    endif
    if (icnt >= ibnd) goto bank
        abnd Vocoder as,an,kmin,kmax,kq,ibnd,icnt+1
    bank:
        kfreq = kmin*(kmax/kmin)^((icnt-1)/(ibnd-1))
        kbw = kfreq/kq
        ao VocBand as,an,kfreq,kbw
        amix = ao + abnd
        xout amix
endop

instr 108 ; VOCODER

    ifreq cpspch p5
    p3 = p3*2

    seed 0
    S1 = "plugs.wav"
    imin = 100
    imax = 10000
    iskip = random(0,9)
    ; kenv madsr 0.1,0.1,0.7,0.1
    ;kenv expseg 0.001,0.01,p4+0.001,p3-0.02,p4+0.001,0.01,0.001
    kenv linseg 0,0.01,p4,p3-0.11,p4,0.1,0
    asig diskin2 S1,1,iskip,1
    ; kthresh = -90
    ; kloknee = -50
    ; khiknee = -30
    ; kratio  = 3
    ; katt    = 0.1
    ; krel    = .5
    ; ilook   = .02
    ; asig  compress2 asig, asig, kthresh, kloknee, khiknee, kratio, katt, krel, ilook
    ;asig loscil 1,1,73,1,1
    ;ap,aloc plltrack asig,0.1
    krms port rms(asig),0.01
    ;anoi vco krms,ap,1,0,-1
    anoi vco krms,ifreq,1,0,-1
    aout Vocoder anoi,asig,imin,imax,10,30

    chnmix (aout*3+asig*0.7)*p6*kenv, "mixl"
    chnmix (aout*3+asig*0.7)*p6*kenv, "mixr"
endin

instr 109 ; WURLITZER

    kfreq = cpspch(p5)
    kc1 = random(1,1.3)
    kc2 = 0.3
    kvdepth = 0.35
    kvrate = 5
    ifn1 = -1
    ifn2 = -1
    ifn3 = -1
    ifn4 = 53
    ivfn = -1
    ;kenv expseg 0.00001,0.01,p4,p3-0.02,p4,0.01,0.00001
    kenv linseg 0,0.01,p4,p3-0.11,p4,0.1,0
    asig fmwurlie p4*kenv, kfreq, kc1, kc2, kvdepth, kvrate, ifn1, ifn2, ifn3, ifn4, ivfn
    chnmix asig*p6*0.3, "mixl"
	chnmix asig*p6*0.3, "mixr"

endin

instr 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72 ; DRUMS
    p3=4
    p5 = p5
	if ftchnls(p1) == 1 then
		asigl loscil p4, 1, p1, 1, 0
		asigr = asigl
	elseif ftchnls(p1) == 2 then
	    asigl, asigr loscil p4, 1, p1, 1, 0
	endif
	chnmix asigl*p6, "mixl"
	chnmix asigr*p6, "mixr"
endin


instr 1000 ; mixer
    asigl chnget "mixl"
    asigr chnget "mixr"
    ;asigl butterlp asigl, 5000
    ;asigr butterlp asigr, 5000
    areverbl,areverbr freeverb asigl,asigr,0.6,0.7
    outs asigl*1+areverbl*1.5,asigr*1+areverbr*1.5
    ; outs asigl,asigr
    chnclear "mixl"
    chnclear "mixr"
endin

</CsInstruments>
<CsScore>
f 1 0 0 1 "drums/tr808/BD2510.WAV" 0 0 0
f 2 0 0 1 "drums/tr808/SD0010.WAV" 0 0 0
f 3 0 0 1 "drums/tr808/CH.WAV" 0 0 0
f 4 0 0 1 "drums/tr808/OH00.WAV" 0 0 0
f 5 0 0 1 "drums/tr808/MT00.WAV" 0 0 0
f 6 0 0 1 "drums/tr808/CY0050.WAV" 0 0 0
f 7 0 0 1 "drums/tr808/RS.WAV" 0 0 0
f 8 0 0 1 "drums/tr808/LT50.WAV" 0 0 0
f 9 0 0 1 "drums/tr808/CL.WAV" 0 0 0
f 10 0 0 1 "drums/tr808/MA.WAV" 0 0 0
f 11 0 0 1 "drums/tr808/CH.WAV" 0 0 0
f 12 0 0 1 "drums/emu/emu_CHH.wav" 0 0 0
f 13 0 0 1 "drums/emu/emu_Clap.wav" 0 0 0
f 14 0 0 1 "drums/emu/emu_Cowbell.wav" 0 0 0
f 15 0 0 1 "drums/emu/emu_Kick.wav" 0 0 0
f 16 0 0 1 "drums/emu/emu_OHH.wav" 0 0 0
f 17 0 0 1 "drums/emu/emu_Ride.wav" 0 0 0
f 18 0 0 1 "drums/emu/emu_Rim.wav" 0 0 0
f 19 0 0 1 "drums/emu/emu_Snare.wav" 0 0 0
f 20 0 0 1 "drums/emu/emu_Tom1.wav" 0 0 0
f 21 0 0 1 "drums/emu/emu_Tom2.wav" 0 0 0
f 22 0 0 1 "drums/emu/emu_Tom3.wav" 0 0 0
f 23 0 0 1 "drums/emu/emu_Wood_Block.wav" 0 0 0
f 24 0 0 1 "drums/linn/linn_cabasa.wav" 0 0 0
f 25 0 0 1 "drums/linn/linn_clap.wav" 0 0 0
f 26 0 0 1 "drums/linn/linn_conga_hi.wav" 0 0 0
f 27 0 0 1 "drums/linn/linn_conga_low.wav" 0 0 0
f 28 0 0 1 "drums/linn/linn_cowbell.wav" 0 0 0
f 29 0 0 1 "drums/linn/linn_hat_open.wav" 0 0 0
f 30 0 0 1 "drums/linn/linn_hat_close.wav" 0 0 0
f 31 0 0 1 "drums/linn/linn_hat_med.wav" 0 0 0
f 32 0 0 1 "drums/linn/linn_hat_open.wav" 0 0 0
f 33 0 0 1 "drums/linn/linn_kick.wav" 0 0 0
f 34 0 0 1 "drums/linn/linn_ride.wav" 0 0 0
f 35 0 0 1 "drums/linn/linn_sidestick.wav" 0 0 0
f 36 0 0 1 "drums/linn/linn_snare.wav" 0 0 0
f 37 0 0 1 "drums/linn/linn_tambourine.wav" 0 0 0
f 38 0 0 1 "drums/linn/linn_tom1.wav" 0 0 0
f 39 0 0 1 "drums/linn/linn_tom2.wav" 0 0 0
f 40 0 0 1 "drums/linn/linn_tom3.wav" 0 0 0
f 41 0 0 1 "drums/oberheim/oberheim_hat_accent.wav" 0 0 0
f 42 0 0 1 "drums/oberheim/oberheim_hat_closed.wav" 0 0 0
f 43 0 0 1 "drums/oberheim/oberheim_hat_open.wav" 0 0 0
f 44 0 0 1 "drums/oberheim/oberheim_kick.wav" 0 0 0
f 45 0 0 1 "drums/oberheim/oberheim_ride.wav" 0 0 0
f 46 0 0 1 "drums/oberheim/oberheim_shake.wav" 0 0 0
f 47 0 0 1 "drums/oberheim/oberheim_snare.wav" 0 0 0
f 48 0 0 1 "drums/oberheim/oberheim_stick.wav" 0 0 0
f 49 0 0 1 "drums/oberheim/oberheim_tamborine.wav" 0 0 0
f 50 0 0 1 "drums/oberheim/oberheim_tom1.wav" 0 0 0
f 51 0 0 1 "drums/oberheim/oberheim_tom2.wav" 0 0 0
f 52 0 0 1 "drums/oberheim/oberheim_tom3.wav" 0 0 0
f 53 0 256 1 "drums/fwavblnk.aiff" 0 0 0 ;RHODES
f 54 0 256 1 "drums/marmstk1.wav" 0 0 0 ;MARIMBA
f 55 0 0 1 "drums/cr78/cr78_Bongo_High.wav" 0 0 0
f 56 0 0 1 "drums/cr78/cr78_Bongo_Low.wav" 0 0 0
f 57 0 0 1 "drums/cr78/cr78_Conga_Low.wav" 0 0 0
f 58 0 0 1 "drums/cr78/cr78_Cymbal.wav" 0 0 0
f 59 0 0 1 "drums/cr78/cr78_Guiro_Short.wav" 0 0 0
f 60 0 0 1 "drums/cr78/cr78_Hat_Closed.wav" 0 0 0
f 61 0 0 1 "drums/cr78/cr78_Hi_Hat.wav" 0 0 0
f 62 0 0 1 "drums/cr78/cr78_Kick3.wav" 0 0 0
f 63 0 0 1 "drums/cr78/cr78_Rim_Shot.wav" 0 0 0
f 64 0 0 1 "drums/cr78/cr78_Snare.wav" 0 0 0
f 65 0 0 1 "drums/cr78/cr78_Tamb1.wav" 0 0 0
f 66 0 0 1 "drums/univox/univox_CHH.wav" 0 0 0
f 67 0 0 1 "drums/univox/univox_Guiro_Short.wav" 0 0 0
f 68 0 0 1 "drums/univox/univox_Kick.wav" 0 0 0
f 69 0 0 1 "drums/univox/univox_Perc1.wav" 0 0 0
f 70 0 0 1 "drums/univox/univox_Perc2.wav" 0 0 0
f 71 0 0 1 "drums/univox/univox_Quijada.wav" 0 0 0
f 72 0 0 1 "drums/univox/univox_Snare2.wav" 0 0 0
f 73 0 0 1 "plugs.wav" 0 0 0
i 1000 0 -1
