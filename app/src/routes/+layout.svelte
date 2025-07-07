<script lang="ts">
    import '../app.css';
    import '../styles/global.css';
    import '../styles/layout.scss';
    
    let { children } = $props();
</script>

<nav>
    <h4>created by AleK</h4>
</nav>

{@render children()}
