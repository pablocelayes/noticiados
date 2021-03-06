#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from models import *
# from django.contrib import messages


#  Vistas
def start(request):
    init_state()
    return render(request, 'start.html', {})

def preguntando(request, respuesta=None):
    # Si respuesta es no nulo
    # viene de una pregunta anterior (ver state)
    state =  get_state()
    pregunta = proxima_pregunta(state)
    save_state(state)
    return render(request, 'preguntando.html', {'pregunta': pregunta, 'state': state})

def respuesta(request, respuesta):
    # Si respuesta es no nulo
    # viene de una pregunta anterior (ver state)
    state =  get_state()
    pregunta = pregunta_actual(state)

    respuesta = pregunta["opciones"][int(respuesta)]
    correcta = bool(respuesta.lower() == pregunta["respuesta"].lower())
    if not correcta:
        state['vidas'] -= 1
        state['vidas_string'] = ['', '❤', '❤ ❤'][state['vidas']]
    state['correctas'].append(correcta) 

    fin = bool(len(state['correctas']) == N_PREGS_POR_NIVEL or
                state['vidas'] == 0)
    
    save_state(state)
    return render(request, 'respuesta.html', {'pregunta': pregunta, 'state': state,
                                                'correcta': correcta, 'fin': fin,
                                                'respuesta': respuesta})


def end(request):
    state = get_state()
    nivel = state['nivel']
    correctas = state['correctas']
    incorrectas = [PREGUNTAS_NIVEL[nivel][i] for (i, v) in enumerate(correctas) if not v]

    puntaje = 10.0 - len(incorrectas) * 10.0 / len(correctas)
    for p in incorrectas:
        p['tip'] = p['sugerencias'].values()[0] if 'sugerencias' in p else "https://es.wikipedia.org/wiki/Wikipedia:Portada"

    aprobado = bool(puntaje >= 6)

    save_state(state)
    return render(request, 'end.html', {'state': state, 'puntaje': puntaje, 'aprobado': aprobado,
                                'incorrectas': incorrectas})
