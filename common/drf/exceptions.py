from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):

    response = drf_exception_handler(exc, context)

    # Update the structure of the response data.
    if response is not None:
        customized_response = {}
        customized_response["errors"] = []

        for key, value in response.data.items():
            error = {"field": key, "message": value}
            customized_response["errors"].append(error)

        response.data = customized_response

    return response
