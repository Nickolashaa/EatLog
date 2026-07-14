<script setup lang="ts">
const ports = [
  {
    name: 'Десктоп',
    handle: 'Windows · macOS · Linux',
    desc: 'Полный отчёт за день, таблицы приёмов, профиль и цель. Отсюда включаются уведомления в Telegram.',
    href: 'https://github.com/Nickolashaa/EatLog/releases/latest',
    cta: 'Скачать релиз',
    accent: 'var(--green)',
    glyph: '▭',
    live: false,
  },
  {
    name: 'Веб',
    handle: 'этот сайт',
    desc: 'Тот же дневник в браузере — аккаунт общий, ставить ничего не надо. Записал тут — видно на десктопе.',
    href: '#top',
    cta: 'Ты уже здесь',
    accent: 'var(--mauve)',
    glyph: '◐',
    live: false,
    wip: true,
  },
]
</script>

<template>
  <section id="ports" class="ports">
    <div class="shell">
      <header class="ports__head">
        <div class="section-no" data-reveal>03</div>
        <h2 class="ports__h" data-reveal="60">ГДЕ&nbsp;ЖИВЁТ</h2>
        <p class="ports__lede" data-reveal="120">
          Два входа, один дневник. Веди КБЖУ на десктопе или в браузере —
          аккаунт общий.
        </p>
      </header>

      <div class="ports__grid">
        <a
          v-for="p in ports"
          :key="p.name"
          class="port"
          :href="p.href"
          :target="p.href.startsWith('http') ? '_blank' : undefined"
          :rel="p.href.startsWith('http') ? 'noopener' : undefined"
          :style="{ '--a': p.accent }"
          data-magnet
          data-reveal
        >
          <div class="port__top">
            <span class="port__glyph" aria-hidden="true">{{ p.glyph }}</span>
            <span v-if="p.live" class="port__live">● ONLINE</span>
            <span v-else-if="p.wip" class="port__soon">◷ СКОРО</span>
          </div>
          <h3 class="port__name">{{ p.name }}</h3>
          <div class="port__handle">{{ p.handle }}</div>
          <p class="port__desc">{{ p.desc }}</p>
          <div v-if="p.wip" class="port__wip">В&nbsp;разработке</div>
          <div v-else class="port__cta">
            {{ p.cta }} <span aria-hidden="true">↗</span>
          </div>
        </a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.ports {
  padding: clamp(50px, 8vw, 100px) 0 clamp(40px, 6vw, 70px);
}
.ports__head {
  display: grid;
  grid-template-columns: auto auto 1fr;
  align-items: end;
  gap: 24px;
  margin-bottom: clamp(26px, 4vw, 48px);
}
.ports__h {
  font-family: var(--disp);
  font-weight: 900;
  font-size: clamp(30px, 6vw, 68px);
  line-height: 0.9;
  letter-spacing: -0.03em;
  text-transform: uppercase;
}
.ports__lede {
  color: var(--muted);
  font-size: 14px;
  line-height: 1.6;
  max-width: 40ch;
  justify-self: end;
  text-align: right;
}

.ports__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: clamp(16px, 2.4vw, 26px);
}
.port {
  display: flex;
  flex-direction: column;
  border: var(--edge) solid var(--text);
  background: var(--bg-2);
  padding: 22px;
  box-shadow: 7px 7px 0 var(--ink);
  transition: transform 0.14s ease, box-shadow 0.14s ease, background 0.14s ease;
}
.port:hover {
  transform: translate(-3px, -3px);
  box-shadow: 10px 10px 0 var(--a);
  background: var(--bg-3);
}
.port:active {
  transform: translate(2px, 2px);
  box-shadow: 0 0 0 var(--a);
}
.port__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.port__glyph {
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  border: var(--edge) solid var(--text);
  background: var(--a);
  color: var(--crust);
  font-size: 22px;
  box-shadow: 3px 3px 0 var(--ink);
}
.port__live {
  font-family: var(--mono);
  font-weight: 700;
  font-size: 10px;
  letter-spacing: 0.16em;
  color: var(--green);
}
.port__soon {
  font-family: var(--mono);
  font-weight: 700;
  font-size: 10px;
  letter-spacing: 0.16em;
  color: var(--yellow);
}
.port__name {
  font-family: var(--disp);
  font-weight: 900;
  font-size: 27px;
  letter-spacing: -0.02em;
  text-transform: uppercase;
}
.port__handle {
  font-family: var(--mono);
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.06em;
  color: var(--a);
  margin: 4px 0 12px;
}
.port__desc {
  color: var(--muted);
  font-size: 14px;
  line-height: 1.58;
  flex: 1;
}
.port__cta {
  margin-top: 18px;
  padding-top: 14px;
  border-top: 2px dashed var(--border);
  font-family: var(--mono);
  font-weight: 800;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text);
  display: flex;
  justify-content: space-between;
}
.port:hover .port__cta span {
  color: var(--a);
}
.port__wip {
  margin-top: 18px;
  padding: 11px 14px;
  border: 2px solid var(--ink);
  background: var(--yellow);
  color: var(--crust);
  font-family: var(--mono);
  font-weight: 800;
  font-size: 12px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  text-align: center;
  box-shadow: 3px 3px 0 var(--ink);
}

@media (max-width: 860px) {
  .ports__grid {
    grid-template-columns: 1fr;
  }
  .ports__head {
    grid-template-columns: auto 1fr;
  }
  .ports__lede {
    grid-column: 1 / -1;
    justify-self: start;
    text-align: left;
  }
}
</style>
