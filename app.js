'use strict';
(() => {
 const works = JSON.parse(document.querySelector('#work-data').textContent);
 const dialog = document.querySelector('#work-dialog');
 const picture = document.querySelector('#dialog-image');
 let active = 0;
 let view = 0;
 let opener = null;
 const byId = id => works.findIndex(work => work.id === id);
 const path = (slug, size = 'full') => `assets/images/${slug}-${size}.webp`;
 const bilingual = (element, chinese, english) => {
  element.textContent = chinese;
  const translation = document.createElement('span');
  translation.className = 'en';
  translation.lang = 'en';
  translation.textContent = english;
  element.append(translation);
 };

 function renderView(index) {
  view = index;
  const work = works[active];
  const image = work.images[view];
  picture.src = path(image.slug);
  picture.alt = `${work.title} / ${work.title_en} · ${image.label} / ${image.label_en}`;
  document.querySelector('#original-image-link').href = path(image.slug);
  document.querySelector('#source-page-link').href = `assets/chen-guojun-selected-works.pdf#page=${image.page}`;
  bilingual(document.querySelector('#dialog-source'), `${image.label} / 原始图录第 ${image.page} 页`, `${image.label_en} / Source catalogue, page ${image.page}`);
  dialog.querySelectorAll('.view-thumb').forEach((button, i) => button.setAttribute('aria-pressed', String(i === view)));
 }

 function renderWork(index, initialView = 0) {
  active = (index + works.length) % works.length;
  const work = works[active];
  bilingual(document.querySelector('#dialog-title'), work.title + (work.subtitle ? `（${work.subtitle}）` : ''), work.title_en + (work.subtitle_en ? ` (${work.subtitle_en})` : ''));
  bilingual(document.querySelector('#dialog-category'), work.category, work.category_en);
  bilingual(document.querySelector('#dialog-description'), work.description, work.description_en);
  document.querySelector('#dialog-counter').textContent = `作品 / Work ${String(active + 1).padStart(2, '0')} / ${String(works.length).padStart(2, '0')}`;
  const views = document.querySelector('#dialog-views');
  views.replaceChildren();
  if (work.images.length > 1) work.images.forEach((image, i) => {
   const button = document.createElement('button');
   button.type = 'button';
   button.className = 'view-thumb';
   button.setAttribute('aria-label', `${image.label} / ${image.label_en}`);
   const thumbnail = document.createElement('img');
   thumbnail.src = path(image.slug, 'preview');
   thumbnail.alt = `${image.label} / ${image.label_en}`;
   button.append(thumbnail);
   button.addEventListener('click', () => renderView(i));
   views.append(button);
  });
  renderView(Math.min(initialView, work.images.length - 1));
 }

 document.querySelectorAll('[data-open]').forEach(button => button.addEventListener('click', () => {
  opener = button;
  const card = button.closest('.work-card');
  const pressed = card?.querySelector('[data-variant][aria-pressed="true"]');
  renderWork(byId(button.dataset.open), pressed ? Number(pressed.dataset.variant) : 0);
  dialog.showModal();
 }));
 document.querySelectorAll('[data-variant]').forEach(button => button.addEventListener('click', () => {
  const work = works[byId(button.dataset.work)];
  const index = Number(button.dataset.variant);
  const card = button.closest('.work-card');
  const image = card.querySelector('.work-visual .image-button img');
  image.src = path(work.images[index].slug, 'preview');
  image.alt = `${work.title} / ${work.title_en} · ${work.images[index].label} / ${work.images[index].label_en}`;
  card.querySelectorAll('[data-variant]').forEach(other => other.setAttribute('aria-pressed', String(other === button)));
 }));
 document.querySelector('.close-dialog').addEventListener('click', () => dialog.close());
 dialog.addEventListener('click', event => {
  const r = dialog.getBoundingClientRect();
  if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close();
 });
 dialog.addEventListener('close', () => opener?.focus({preventScroll: true}));
 document.querySelector('#previous-work').addEventListener('click', () => renderWork(active - 1));
 document.querySelector('#next-work').addEventListener('click', () => renderWork(active + 1));
 dialog.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft') { event.preventDefault(); renderWork(active - 1); }
  if (event.key === 'ArrowRight') { event.preventDefault(); renderWork(active + 1); }
 });
})();
