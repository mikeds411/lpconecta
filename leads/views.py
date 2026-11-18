from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .forms import AgendamentoForm, ContatoForm


@ensure_csrf_cookie
def home(request):
    return render(request, "index.html")


def _meta(request):
    fwd = request.META.get("HTTP_X_FORWARDED_FOR", "")
    ip = fwd.split(",")[0].strip() or request.META.get("REMOTE_ADDR")
    return {
        "ip": ip or None,
        "user_agent": request.META.get("HTTP_USER_AGENT", "")[:300],
        "origem": request.META.get("HTTP_REFERER", "")[:300],
    }


def _salvar(request, form_cls):
    form = form_cls(request.POST)
    if form.is_bot():
        return None, JsonResponse({"ok": True})  # finge sucesso para o robô
    if not form.is_valid():
        erros = {k: v[0] for k, v in form.errors.items()}
        return None, JsonResponse({"ok": False, "erros": erros}, status=400)
    obj = form.save(commit=False)
    for k, v in _meta(request).items():
        setattr(obj, k, v)
    obj.save()
    return obj, None


@require_POST
def agendamento(request):
    obj, erro = _salvar(request, AgendamentoForm)
    if erro:
        return erro
    return JsonResponse({"ok": True, "protocolo": obj.protocolo})


@require_POST
def contato(request):
    obj, erro = _salvar(request, ContatoForm)
    if erro:
        return erro
    return JsonResponse({"ok": True})
