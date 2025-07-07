<script lang="ts">
  import Button from "@/lib/components/ui/button/button.svelte";
  import Meteors from "@/lib/components/ui/meteors.svelte";

</script>

<div class="relative w-screen h-screen">
    <Meteors number={50}/>
    <div class="absolute left-1/2 top-1/2 flex justify-center items-center w-2/5 h-2/5 gap-5 flex-col -translate-x-1/2 -translate-y-1/2">
        <h1 class="w-full text-center text-3xl">Learning indonesia word by Audio</h1>
        <Button class="px-5 w-2/5 cursor-pointer hover:bg-white hover:text-[var(--secondary)] hover:border-[var(--secondary)] border-2 transition-all duration-500">Start Game</Button>
        <p class="text-[var(--secondary)] hover:scale-125 transition-all cursor-pointer">How to <b>Play</b>?</p>
    </div>
</div>


<style>
    h1{
        font-family: 'Poppins-SemiBold', sans-serif;
    }
</style>