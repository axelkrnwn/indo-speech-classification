<script lang="ts">
    let { children } = $props();
</script>

<nav>
    <h4>created by AleK</h4>
</nav>

{@render children()}

<style lang="scss">
    :global(*){
      margin: 0;
      padding: 0;
    }

    :global(:root){
        --white:#FFF1D5;
        --primary:#48A6A7;
        --secondary:#006A71;
        --accent:#9ACBD0;
        --black: #1b1b1b;
    }

    @font-face {
        font-family: 'Poppins-Regular';
        src: url('../asset/font/Poppins-Regular.ttf');
    }
    @font-face {
        font-family: 'Poppins-Light';
        src: url('../asset/font/Poppins-Light.ttf');
    }
    @font-face {
        font-family: 'Poppins-Semibold';
        src: url('../asset/font/Poppins-SemiBold.ttf');
    }
    @font-face {
        font-family: 'Poppins-Bold';
        src: url('../asset/font/Poppins-Bold.ttf');
    }

    nav{
        box-sizing: border-box;
        padding: 3vh 2vw;
        width: 100vw;
        display: flex;
        justify-content: right;
        h4{
            color: var(--secondary);
            font-size: 1.1rem;
            font-family: 'Poppins-Light', sans-serif;
        }
    }
</style>