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
 const english = document.documentElement.lang === 'en';
 const text = (chinese, translated) => english ? translated : chinese;
 const field = (item, name) => item[english ? `${name}_en` : name];

 function renderView(index) {
  view = index;
  const work = works[active];
  const image = work.images[view];
  picture.src = path(image.slug);
  picture.alt = `${field(work, 'title')} · ${field(image, 'label')}`;
  document.querySelector('#original-image-link').href = path(image.slug);
  document.querySelector('#source-page-link').href = `assets/chen-guojun-selected-works.pdf#page=${image.page}`;
  document.querySelector('#dialog-source').textContent = text(`${image.label} / 原始图录第 ${image.page} 页`, `${image.label_en} / Source catalogue, page ${image.page}`);
  dialog.querySelectorAll('.view-thumb').forEach((button, i) => button.setAttribute('aria-pressed', String(i === view)));
 }

 function renderWork(index, initialView = 0) {
  active = (index + works.length) % works.length;
  const work = works[active];
  document.querySelector('#dialog-title').textContent = field(work, 'title') + (work.subtitle ? text(`（${work.subtitle}）`, ` (${work.subtitle_en})`) : '');
  document.querySelector('#dialog-category').textContent = field(work, 'category');
  document.querySelector('#dialog-description').textContent = field(work, 'description');
  document.querySelector('#dialog-counter').textContent = `${text('作品', 'Work')} ${String(active + 1).padStart(2, '0')} / ${String(works.length).padStart(2, '0')}`;
  const views = document.querySelector('#dialog-views');
  views.replaceChildren();
  if (work.images.length > 1) work.images.forEach((image, i) => {
   const button = document.createElement('button');
   button.type = 'button';
   button.className = 'view-thumb';
   button.setAttribute('aria-label', field(image, 'label'));
   const thumbnail = document.createElement('img');
   thumbnail.src = path(image.slug, 'preview');
   thumbnail.alt = field(image, 'label');
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
  image.alt = `${field(work, 'title')} · ${field(work.images[index], 'label')}`;
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
