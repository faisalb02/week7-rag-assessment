def check_faithfulness(answer_claims, context):

    results = []

    for claim in answer_claims:

        if claim.lower() in context.lower():

            results.append({
                "claim": claim,
                "status": "SUPPORTED"
            })

        else:

            results.append({
                "claim": claim,
                "status": "UNSUPPORTED"
            })

    return results