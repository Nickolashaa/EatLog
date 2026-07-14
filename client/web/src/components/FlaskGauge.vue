<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'

const props = defineProps<{
  label: string
  unit: string
  color: string
  index: number
}>()

const shown = ref(0)
const el = ref<HTMLElement | null>(null)

function randTarget() {
  return Math.floor(Math.random() * 90) + 10
}

let raf = 0
let started = false

function run() {
  if (started) return
  started = true
  const from = 0
  const to = randTarget()
  const dur = 1050
  const t0 = performance.now() + props.index * 130
  const step = (now: number) => {
    const p = Math.max(0, Math.min(1, (now - t0) / dur))
    const eased = 1 - Math.pow(1 - p, 2.4)
    shown.value = Math.round(from + (to - from) * eased)
    if (p < 1) raf = requestAnimationFrame(step)
    else shown.value = to
  }
  raf = requestAnimationFrame(step)
}

function repour() {
  cancelAnimationFrame(raf)
  shown.value = 0
  started = false
  run()
}

let io: IntersectionObserver | null = null
onMounted(() => {
  if (!el.value) return
  io = new IntersectionObserver(
    (entries) => {
      for (const e of entries) if (e.isIntersecting) run()
    },
    { threshold: 0.4 },
  )
  io.observe(el.value)
})
onBeforeUnmount(() => {
  cancelAnimationFrame(raf)
  io?.disconnect()
})
</script>

<template>
  <div
    ref="el"
    class="fg"
    :style="{ '--c': color }"
    data-magnet
    role="button"
    tabindex="0"
    :aria-label="`${label}: ${shown} ${unit}`"
    @click="repour"
    @keydown.enter.prevent="repour"
    @keydown.space.prevent="repour"
  >
    <div class="fg__top">
      <span class="fg__name">{{ label }}</span>
      <span class="fg__pct">{{ shown }}%</span>
    </div>

    <div class="fg__flask">
      <div class="fg__ticks" aria-hidden="true"></div>
      <div class="fg__fill" :style="{ height: shown + '%' }">
        <span class="fg__surface"></span>
      </div>
      <div class="fg__readout">
        <b>{{ shown }}</b>
        <span class="fg__unit">{{ unit }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fg {
  display: flex;
  flex-direction: column;
  min-width: 0;
  user-select: none;
  outline: none;
}
.fg:focus-visible .fg__flask {
  box-shadow: 0 0 0 3px var(--bg), 0 0 0 6px var(--c);
}

.fg__top {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 6px;
  margin-bottom: 8px;
}
.fg__name {
  font-family: var(--mono);
  font-weight: 800;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text);
}
.fg__pct {
  font-family: var(--mono);
  font-weight: 700;
  font-size: 12px;
  color: var(--c);
}

.fg__flask {
  position: relative;
  height: clamp(150px, 20vh, 190px);
  border: 4px solid var(--text);
  border-radius: 20px;
  background: var(--bg-3);
  overflow: hidden;
  transition: transform 0.14s ease, box-shadow 0.14s ease;
}
.fg:hover .fg__flask {
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0 var(--c);
}
.fg:active .fg__flask {
  transform: translate(2px, 2px);
  box-shadow: 0 0 0 var(--c);
}

.fg__ticks {
  position: absolute;
  left: 0;
  top: 10px;
  bottom: 10px;
  width: 15px;
  z-index: 3;
  background: repeating-linear-gradient(
    to top,
    transparent 0 21px,
    var(--dim) 21px 22px
  );
  opacity: 0.9;
}

.fg__fill {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--c);
  height: 0;
  z-index: 1;
}
.fg__surface {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: #ffffff;
  opacity: 0.55;
}

.fg__readout {
  position: absolute;
  z-index: 4;
  left: 0;
  right: 0;
  bottom: 12px;
  text-align: center;
  mix-blend-mode: difference;
  color: #ffffff;
}
.fg__readout b {
  font-family: var(--disp);
  font-weight: 800;
  font-size: clamp(32px, 3.6vw, 48px);
  line-height: 1;
  letter-spacing: -0.03em;
}
.fg__unit {
  display: block;
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-top: 2px;
}
</style>
