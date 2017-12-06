from automated_survey.models import Survey, Question
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse


@require_GET
def show_survey_results(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    responses_to_render = [response.as_dict() for response in survey.responses]

    unique_phone_numbers = []
    #split out responses_to_render by phone number and feed an array of dicts to template instead
    for response in responses_to_render:
        if response["phone_number"] not in unique_phone_numbers:
            unique_phone_numbers.append(response["phone_number"])

    truncated_unique_phone_numbers = []
    for phone in unique_phone_numbers:
        truncated_unique_phone_numbers.append(phone[1:])

    template_context = {
        'responses': truncated_unique_phone_numbers,
        'survey_title': survey.title,
        'survey_id': survey_id
    }

    return render_to_response('results.html', context=template_context)

@require_GET
def show_survey_detail(request, survey_id, phone):
    survey = Survey.objects.get(id=survey_id)
    responses_to_render = [response.as_dict() for response in survey.responses]

    print(responses_to_render)

    responses_to_show = []
    for response in responses_to_render:
        if response["phone_number"] == '+' + phone:
            responses_to_show.append(response)

    sorted_responses = sorted(responses_to_show, key=lambda response: response['id'])

    template_context = {
        'survey_title': survey.title,
        'responses': sorted_responses
    }
    return render_to_response('survey_detail.html', context=template_context)

@csrf_exempt
def show_survey(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    first_question = survey.first_question

    first_question_ids = {
        'survey_id': survey.id,
        'question_id': first_question.id
    }

    first_question_url = reverse('question', kwargs=first_question_ids)

    welcome = 'Hello! Thank you for contacting Ivy Global United, the premier advocacy organization for surrogates. You are about to take the %s survey' % survey.title
    if request.is_sms:
        twiml_response = MessagingResponse()
        twiml_response.message(welcome)
        twiml_response.redirect(first_question_url, method='GET')
    else:
        twiml_response = VoiceResponse()
        twiml_response.say(welcome)
        twiml_response.redirect(first_question_url, method='GET')

    return HttpResponse(twiml_response, content_type='application/xml')


@require_POST
def redirects_twilio_request_to_proper_endpoint(request):
    answering_question = request.session.get('answering_question_id')
    # answering_question = False #uncomment this for restarting interview loop -- remember to comment out after right after restarting
    if not answering_question:
        second_survey = Survey.objects.all()[0]
        redirect_url = reverse('survey',
                               kwargs={'survey_id': second_survey.id})
    else:
        question = Question.objects.get(id=answering_question)
        redirect_url = reverse('save_response',
                               kwargs={'survey_id': question.survey.id,
                                       'question_id': question.id})
    return HttpResponseRedirect(redirect_url)


@require_GET
def redirect_to_first_results(request):
    second_survey = Survey.objects.all()[0]
    results_for_first_survey = reverse(
        'survey_results', kwargs={
            'survey_id': second_survey.id})
    return HttpResponseRedirect(results_for_first_survey)
