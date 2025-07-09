<script lang="ts">
    import Button from "@/lib/components/ui/button/button.svelte";
    import Meteors from "@/lib/components/ui/meteors.svelte";
  import { sendBlobAsFile } from "@/lib/sender";
  import { onMount } from "svelte";

    let media:Blob[] = $state([]);
    let mediaRecorder:MediaRecorder
    let isRecording = $state(false);
    let audioContext:AudioContext;
    let analyser:AnalyserNode;
    let source;
    let dataArray:Uint8Array;
    let silenceTimeout = 2000;
    let result: string = $state('')

    const getVolume = () => {
        analyser.getByteFrequencyData(dataArray)
  
        let sum = 0;
        for (const amplitude of dataArray) {
        sum += amplitude * amplitude
        }

        const volume = Math.sqrt(sum / dataArray.length)
        return volume
    }
    
    const onStart = async () => {
        if (!mediaRecorder){
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = (e) => media.push(e.data);
            
            audioContext = new AudioContext();
            source = audioContext.createMediaStreamSource(stream);
            analyser = audioContext.createAnalyser();
            analyser.fftSize = 512;
            dataArray = new Uint8Array(analyser.fftSize);
            source.connect(analyser);
            mediaRecorder.start();
            console.log('start')
            isRecording = true
        }
    }

    const track = () => {

        if (isRecording){
            let volume = getVolume()
            if (volume > 50) {
                console.log('keep going')
                isRecording = true
                clearTimeout(silenceTimeout);
                silenceTimeout = setTimeout(async () => {
                    console.log('stopped')
                    const blob = new Blob(media, { type: 'audio/webm' });
                    media = [];
                    isRecording = false
                    let res = await sendBlobAsFile(blob) 
                    result = JSON.stringify(res);
                    console.log('done predict', result)
                    
                }, 2000);
            }
        }

        requestAnimationFrame(track)
    }

    onMount(() => {
        track()
    })

</script>

<div class="relative w-screen h-screen">
    <Meteors number={50}/>
    <div class="absolute left-1/2 top-1/2 flex justify-center items-center w-2/5 h-2/5 gap-5 flex-col -translate-x-1/2 -translate-y-1/2">
        <h1 class="w-full text-center text-3xl">Learning indonesia word by Audio</h1>
        {isRecording}
        {result}
        <Button onclick={onStart} class="px-5 w-2/5 cursor-pointer hover:bg-white hover:text-[var(--secondary)] hover:border-[var(--secondary)] border-1 transition-all duration-500">Start Game</Button>
        <p class="text-[var(--secondary)] hover:scale-125 transition-all cursor-pointer">How to <b>Play</b>?</p>
    </div>
</div>


<style>
    h1{
        font-family: 'Poppins-SemiBold', sans-serif;
    }
</style>