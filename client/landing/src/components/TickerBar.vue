<script setup lang="ts">
defineProps<{ items: string[]; accent?: string; reverse?: boolean }>()
</script>

<template>
  <div class="ticker" :style="{ '--tk': accent || 'var(--mauve)' }" role="presentation">
    <div class="ticker__track" :class="{ 'ticker__track--rev': reverse }">
      <template v-for="n in 2" :key="n">
        <span v-for="(it, i) in items" :key="n + '-' + i" class="ticker__item">
          {{ it }}<b aria-hidden="true">✦</b>
        </span>
      </template>
    </div>
  </div>
</template>

<style scoped>
.ticker {
  border-block: var(--edge) solid var(--text);
  background: var(--tk);
  color: var(--crust);
  overflow: hidden;
  white-space: nowrap;
}
.ticker__track {
  display: inline-flex;
  align-items: center;
  padding-block: 11px;
  animation: slide 26s linear infinite;
}
.ticker__track--rev {
  animation-direction: reverse;
}
.ticker:hover .ticker__track {
  animation-play-state: paused;
}
.ticker__item {
  font-family: var(--disp);
  font-weight: 800;
  font-size: 15px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding-inline: 22px;
  display: inline-flex;
  align-items: center;
  gap: 22px;
}
.ticker__item b {
  color: color-mix(in srgb, var(--crust) 55%, var(--tk));
  font-size: 13px;
}
@keyframes slide {
  to {
    transform: translateX(-50%);
  }
}
@media (prefers-reduced-motion: reduce) {
  .ticker__track {
    animation: none;
  }
}
</style>
