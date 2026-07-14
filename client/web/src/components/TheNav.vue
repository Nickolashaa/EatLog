<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from 'vue'

const stuck = ref(false)
function onScroll() {
  stuck.value = window.scrollY > 12
}
onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onBeforeUnmount(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <header class="nav" :class="{ 'nav--stuck': stuck }">
    <div class="nav__in shell">
      <a href="#top" class="brand" data-magnet aria-label="EatLog — на верх">
        <span class="brand__mark">🥪</span>
        <span class="brand__word">EAT<span>·</span>LOG</span>
      </a>

      <nav class="nav__links" aria-label="Разделы">
        <a href="#protocol" data-magnet><i>01</i> протокол</a>
        <a href="#label" data-magnet><i>02</i> состав</a>
        <a href="#ports" data-magnet><i>03</i> платформы</a>
      </nav>

      <a
        class="nav__cta"
        href="https://github.com/Nickolashaa/EatLog/releases/latest"
        target="_blank"
        rel="noopener"
        data-magnet
      >
        Скачать
        <span class="nav__cta-dot" aria-hidden="true"></span>
      </a>
    </div>
  </header>
</template>

<style scoped>
.nav {
  position: sticky;
  top: 0;
  z-index: 60;
  border-bottom: var(--edge) solid transparent;
  transition: border-color 0.2s ease, background 0.2s ease;
}
.nav--stuck {
  border-bottom-color: var(--text);
  background: color-mix(in srgb, var(--bg) 82%, transparent);
  backdrop-filter: blur(6px);
}
.nav__in {
  display: flex;
  align-items: center;
  gap: 18px;
  height: 66px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  border: var(--edge) solid var(--text);
  background: var(--bg-2);
  padding: 7px 12px;
  box-shadow: 4px 4px 0 var(--mauve);
}
.brand__mark {
  font-size: 16px;
  line-height: 1;
}
.brand__word {
  font-family: var(--disp);
  font-weight: 900;
  font-size: 16px;
  letter-spacing: 0.02em;
}
.brand__word span {
  color: var(--mauve);
}

.nav__links {
  display: flex;
  gap: 4px;
  margin-left: auto;
}
.nav__links a {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-family: var(--mono);
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  padding: 8px 12px;
  border: 2px solid transparent;
  transition: color 0.14s ease, border-color 0.14s ease;
}
.nav__links a i {
  font-style: normal;
  color: var(--dim);
}
.nav__links a:hover {
  color: var(--text);
  border-color: var(--border);
}

.nav__cta {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  font-family: var(--mono);
  font-weight: 800;
  font-size: 13px;
  color: var(--crust);
  background: var(--green);
  border: var(--edge) solid var(--ink);
  padding: 9px 14px;
  box-shadow: 4px 4px 0 var(--ink);
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}
.nav__cta:hover {
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0 var(--ink);
}
.nav__cta:active {
  transform: translate(2px, 2px);
  box-shadow: 0 0 0 var(--ink);
}
.nav__cta-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--crust);
  animation: blip 1.4s steps(1) infinite;
}
@keyframes blip {
  50% {
    opacity: 0.15;
  }
}

@media (max-width: 820px) {
  .nav__links {
    display: none;
  }
}
</style>
