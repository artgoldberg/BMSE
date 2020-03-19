# comprehensive version
def dump_results(self, errors=False):
    """ Provide results of test runs

    Args:
        errors (:obj:`bool`, optional): if set, provide results that have errors; otherwise,
            provide results that don't have errors

    Returns:
        :obj:`list` of :obj:`list` of :obj:`obj`: results summarized
    """
    fields = 'simul_type case_num result_type duration'.split()
    formatted_results = []
    for result in self.results:
        # either results with errors, or results without errors
        if errors:
            if result.error:
                # report on errors
                pass
            else:
                continue
        else:
            if result.error:
                continue
            else:
                # results without errors
                row = {}
                row['simul_type'] = result.case_type
                row['case_num'] = result.case_num
                row['result_type'] = result.result_type.name
                row['duration'] = result.duration
                if result.output:
                    params = eval(result.output)
                    params = DictUtil.flatten_dict(params)
                    for k, v in params.items():
                        row[k] = v
                formatted_results.append(row)

    return formatted_results

# simplifications noted
def dump_results(self, errors=False):
    """ Provide results of test runs

    Args:
        errors (:obj:`bool`, optional): if set, provide results that have errors; otherwise,
            provide results that don't have errors

    Returns:
        :obj:`list` of :obj:`list` of :obj:`obj`: results summarized
    """
    fields = 'simul_type case_num result_type duration'.split()
    formatted_results = []
    for result in self.results:
        # either results with errors, or results without errors
        # SIMPLIFY: combine nested ifs with 'and'
        if errors and result.error:
            # report on errors
            pass
            # SIMPLIFY: 'else' not needed
            # SIMPLIFY: combine 'else' and 'if'
            # SIMPLIFY: remove 'elif result.error:' and move continue after it here
            continue
        # FIX THIS:
        # SIMPLIFY: 'else' not needed
        # results without errors
        row = {}
        row['simul_type'] = result.case_type
        row['case_num'] = result.case_num
        row['result_type'] = result.result_type.name
        row['duration'] = result.duration
        if result.output:
            params = eval(result.output)
            params = DictUtil.flatten_dict(params)
            for k, v in params.items():
                row[k] = v
        formatted_results.append(row)

    return formatted_results

# what's the difference between list(x) and [x]?
