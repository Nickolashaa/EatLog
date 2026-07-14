<script setup lang="ts">
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { observeReveals } from './directives/reveal'
import TheNav from './components/TheNav.vue'
import SpecHero from './components/SpecHero.vue'
import TickerBar from './components/TickerBar.vue'
import LabProtocol from './components/LabProtocol.vue'
import NutritionPanel from './components/NutritionPanel.vue'
import PlatformsBlock from './components/PlatformsBlock.vue'
import CtaBlock from './components/CtaBlock.vue'
import TheFooter from './components/TheFooter.vue'

const ticker = [
  'БЕЛКИ',
  'ЖИРЫ',
  'УГЛЕВОДЫ',
  'КАЛОРИИ',
  'ДНЕВНИК ПИТАНИЯ',
  'EAT · LOG',
  'СЧИТАЙ КБЖУ',
]
const ticker2 = [
  'ДЕСКТОП',
  'ВЕБ',
  'ОДИН АККАУНТ',
  'НОРМА ДНЯ',
  'УВЕДОМЛЕНИЯ',
  'БЕЗ ДУХОТЫ',
]

const reticle = ref<HTMLElement | null>(null)
let raf = 0
let tx = 0
let ty = 0
let cx = 0
let cy = 0
let stopReveals: (() => void) | null = null

function onMove(e: MouseEvent) {
  tx = e.clientX
  ty = e.clientY
  const hot = !!(e.target as HTMLElement)?.closest(
    'a, button, [data-magnet], [role="button"]',
  )
  reticle.value?.classList.toggle('is-hot', hot)
}

function loop() {
  cx += (tx - cx) * 0.35
  cy += (ty - cy) * 0.35
  if (reticle.value)
    reticle.value.style.transform = `translate(${cx}px, ${cy}px)`
  raf = requestAnimationFrame(loop)
}

onMounted(() => {
  nextTick(() => {
    stopReveals = observeReveals(document)
  })

  const fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches
  if (!fine) return
  document.body.classList.add('has-reticle')
  window.addEventListener('mousemove', onMove, { passive: true })
  raf = requestAnimationFrame(loop)
})
onBeforeUnmount(() => {
  window.removeEventListener('mousemove', onMove)
  cancelAnimationFrame(raf)
  stopReveals?.()
})
</script>

<template>
  <div ref="reticle" class="reticle" aria-hidden="true">
    <span class="reticle__c reticle__c--tl"></span>
    <span class="reticle__c reticle__c--tr"></span>
    <span class="reticle__c reticle__c--bl"></span>
    <span class="reticle__c reticle__c--br"></span>
  </div>

  <TheNav />

  <main>
    <SpecHero />
    <TickerBar :items="ticker" accent="var(--mauve)" />
    <LabProtocol />
    <TickerBar :items="ticker2" accent="var(--green)" reverse />
    <NutritionPanel />
    <PlatformsBlock />
    <CtaBlock />
  </main>

  <TheFooter />
</template>
