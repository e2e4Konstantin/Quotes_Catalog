import inspect


def x__get_selected_tables(selected_chapter: str = '', selected_collection: str = '', selected_section: str = '', selected_subsection: str = '') -> list[str] | None:
    # k = list(locals().keys())
    # v = list(locals().values())
    # print(list(locals().keys()))
    # print(list(locals().values()))
    print(locals())
    # d = locals()
    # d.pop('selected_chapter')
    # print(d)
    # l = d.values()
    # print(l)
    check = lambda x: x == ''                       #and x is not None
    # print(check(''), check(None), check('*'))
    # print(list(map(check, d.values())))
    # print(all(map(check, d.values())))

    if not check(selected_chapter) and check(selected_collection) and check(selected_section) and check(selected_subsection):
        print(f"глава: {selected_chapter!r}")
    else:
        if not check(selected_chapter) and not check(selected_collection) and check(selected_section) and check(selected_subsection):
            print(f"глава & сборник: {selected_chapter} & {selected_collection}")
        else:
            if not check(selected_chapter) and not check(selected_collection) and not check(selected_section) and check(selected_subsection):
                print(f"глава & сборник & отдел: {selected_chapter!r} & {selected_collection!r} & {selected_section!r}")
            else:
                if not check(selected_chapter) and not check(selected_collection) and not check(selected_section) and not check(selected_subsection):
                    print(f"глава & сборник & отдел & раздел: {selected_chapter!r} & {selected_collection!r} & {selected_section!r} & {selected_subsection!r}")

    # print(inspect.getargvalues(f))
    # p = inspect.signature(get_selected_tables).parameters.values()
    table_codes = []
    return table_codes

def get_selected_tables(selected_chapter: str | None = '',
                        selected_collection: str | None = '',
                        selected_section: str | None = '',
                        selected_subsection: str | None = '') -> list[str] | None:
    # print(locals())
    # print(list(locals().keys()))
    # print(list(locals().values()))
    v = list(locals().values())
    check = lambda x: x == ''
    bv = list(map(check, v))

    print(bv, not bv[0] and all(bv[1:]))
    print(bv, not bv[0] and not bv[1] and all(bv[2:]))




    if not check(selected_chapter) and check(selected_collection) and check(selected_section) and check(selected_subsection):
        print(f"глава: {selected_chapter!r}")
    else:
        if not check(selected_chapter) and not check(selected_collection) and check(selected_section) and check(selected_subsection):
            print(f"глава & сборник: {selected_chapter} & {selected_collection}")
        else:
            if not check(selected_chapter) and not check(selected_collection) and not check(selected_section) and check(selected_subsection):
                print(f"глава & сборник & отдел: {selected_chapter!r} & {selected_collection!r} & {selected_section!r}")
            else:
                if not check(selected_chapter) and not check(selected_collection) and not check(selected_section) and not check(selected_subsection):
                    print(f"глава & сборник & отдел & раздел: {selected_chapter!r} & {selected_collection!r} & {selected_section!r} & {selected_subsection!r}")
    table_codes = []
    return table_codes



get_selected_tables("1")
get_selected_tables("1", '1.5')
get_selected_tables("1", '1.5', None)
get_selected_tables("1", '1.5', None, None)
