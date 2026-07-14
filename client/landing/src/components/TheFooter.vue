<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<template>
  <footer class="foot">
    <div class="shell">
      <div class="foot__top">
        <a href="#top" class="foot__brand" data-magnet>
          <span>🥪</span> EAT·LOG
        </a>
        <div class="foot__cols">
          <div>
            <span class="foot__cap">Продукт</span>
            <a href="#protocol" data-magnet>Протокол</a>
            <a href="#label" data-magnet>Состав</a>
            <a href="#ports" data-magnet>Платформы</a>
          </div>
          <div>
            <span class="foot__cap">Входы</span>
            <a href="https://github.com/Nickolashaa/EatLog/releases/latest" target="_blank" rel="noopener" data-magnet>Десктоп</a>
            <a href="#top" data-magnet>Веб</a>
            <a href="https://github.com/Nickolashaa/EatLog" target="_blank" rel="noopener" data-magnet>GitHub</a>
          </div>
          <div>
            <span class="foot__cap">Дневник</span>
            <span class="foot__stat"><i></i>дневник онлайн</span>
            <span class="foot__muted">белки · жиры · углеводы · калории</span>
            <span class="foot__muted">уведомления в Telegram</span>
          </div>
        </div>
      </div>

      <div class="foot__bar">
        <span>© {{ year }} EATLOG — веди КБЖУ без духоты</span>
        <a
          class="foot__sig"
          href="https://github.com/Nickolashaa"
          target="_blank"
          rel="noopener"
          data-magnet
          >Nickolashaa</a
        >
      </div>
    </div>
  </footer>
</template>

<style scoped>
.foot {
  border-top: var(--edge) solid var(--text);
  background: var(--bg-2);
  padding: clamp(36px, 5vw, 60px) 0 22px;
}
.foot__top {
  display: flex;
  flex-wrap: wrap;
  gap: 30px 40px;
  justify-content: space-between;
}
.foot__brand {
  font-family: var(--disp);
  font-weight: 900;
  font-size: clamp(30px, 5vw, 54px);
  letter-spacing: -0.02em;
}
.foot__brand span {
  font-size: 0.7em;
}
.foot__cols {
  display: flex;
  gap: clamp(24px, 5vw, 64px);
  flex-wrap: wrap;
}
.foot__cols > div {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.foot__cap {
  font-family: var(--mono);
  font-weight: 800;
  font-size: 11px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--dim);
  margin-bottom: 4px;
}
.foot__cols a {
  font-family: var(--mono);
  font-weight: 500;
  font-size: 14px;
  color: var(--muted);
  width: fit-content;
  border-bottom: 2px solid transparent;
  transition: color 0.14s, border-color 0.14s;
}
.foot__cols a:hover {
  color: var(--text);
  border-color: var(--mauve);
}
.foot__muted {
  font-family: var(--mono);
  font-size: 14px;
  color: var(--dim);
}
.foot__stat {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--mono);
  font-size: 14px;
  color: var(--green);
}
.foot__stat i {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--green);
  animation: fbl 1.6s steps(1) infinite;
}
@keyframes fbl {
  50% {
    opacity: 0.2;
  }
}
.foot__bar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 20px;
  justify-content: space-between;
  margin-top: clamp(28px, 4vw, 44px);
  padding-top: 18px;
  border-top: 2px dashed var(--border);
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--dim);
}
.foot__sig {
  color: var(--mauve);
  font-weight: 700;
  border-bottom: 2px solid transparent;
  transition: border-color 0.14s ease;
}
.foot__sig:hover {
  border-color: var(--mauve);
}
</style>
