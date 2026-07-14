export function observeReveals(root: ParentNode = document): () => void {
  const nodes = Array.from(root.querySelectorAll<HTMLElement>('[data-reveal]'))

  if (typeof IntersectionObserver === 'undefined') {
    nodes.forEach((n) => n.classList.add('is-revealed'))
    return () => {}
  }

  const io = new IntersectionObserver(
    (entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          e.target.classList.add('is-revealed')
          io.unobserve(e.target)
        }
      }
    },
    { threshold: 0.16, rootMargin: '0px 0px -6% 0px' },
  )

  for (const n of nodes) {
    const delay = Number(n.getAttribute('data-reveal'))
    if (delay) n.style.transitionDelay = `${delay}ms`
    io.observe(n)
  }

  const safety = window.setTimeout(() => {
    nodes.forEach((n) => n.classList.add('is-revealed'))
  }, 2500)

  return () => {
    io.disconnect()
    window.clearTimeout(safety)
  }
}
