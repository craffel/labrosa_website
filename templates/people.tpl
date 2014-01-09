{% include "header.tpl" %}

<h2>People</h2>

{% if people %}
    <table id="peopleTable">
        <tr class="topRow">
            <td>Photo</td>
            <td>Name</td>
            <td>Status</td>
            <td>Research</td>
            <td>Website</td>
        </tr>
    {% for person in people %}
        <tr style="background-color: {{loop.cycle('#FFFFFF', '#EEEEEE') }}">
            <td><img src="{{ person.photo }}" style="height: 100px" /></td>
            <td style="white-space: nowrap">
<script type="text/javascript" language="javascript">
<!--
{
document.write( '<a href="m' + 'a' + 'ilto:' + '{{ person.email|safe }}' + '">' )
}
//-->
</script>{{ person.name }}</a></td>
            <td>{{ person.status }}</td>
            <td>{{ person.research }}</td>
            <td><a href="{{ person.url }}">{{ person.url }}</a></td>
        </tr>
    {% endfor %}
    </table>
{% endif %}

{% include "footer.tpl" %}
